from typing import List
from copy import deepcopy

DEFAULT_COMPONENT_NAME = "(Unnamed)"

class Component:
    def __init__(self, name = DEFAULT_COMPONENT_NAME):
        self.name = name

    def generatePermutations(expected = True):
        return []

class Truth:
    def __init__(self, *mappings: List[bool]):
        self.mappings = mappings

class Permutation:
    def __init__(self, reference: Component, inputPermutations: Component, value = True):
        self.reference = reference
        self.inputPermutations = inputPermutations
        self.value = value

class ReversibleGate(Component):
    def __init__(self, name = DEFAULT_COMPONENT_NAME):
        self.name = name
        self.inputs = []

    def generateTruths(self, expected = True) -> List[Truth]:
        return [Truth(expected)]

    def generatePermutations(self, expected = True) -> List[Permutation]:
        truths = self.generateTruths(expected)
        permutations = []

        for truth in truths:
            inputPermutations = []

            for i in range(0, len(self.inputs)):
                inputPermutations.append(self.inputs[i].generatePermutations(truth.mappings[i]))

            permutations.append(Permutation(self, inputPermutations, expected))

        return permutations

class Input(Component):
    def __init__(self, name = DEFAULT_COMPONENT_NAME):
        super().__init__(name)

        self.name = name
        self.value = None

    def generatePermutations(self, expected = True) -> List[Permutation]:
        return [Permutation(self, [], expected)]

class RAND(ReversibleGate):
    def __init__(self, a, b, name = DEFAULT_COMPONENT_NAME):
        super().__init__(name)

        self.inputs = [a, b]

    def generateTruths(self, expected = True):
        if expected == True:
            return [
                Truth(True, True)
            ]
        else:
            return [
                Truth(False, False),
                Truth(False, True),
                Truth(True, False)
            ]

class ROR(ReversibleGate):
    def __init__(self, a, b, name = DEFAULT_COMPONENT_NAME):
        super().__init__(name)

        self.inputs = [a, b]

    def generateTruths(self, expected = True):
        if expected == True:
            return [
                Truth(False, True),
                Truth(True, False),
                Truth(True, True)
            ]
        else:
            return [
                Truth(False, False)
            ]

class RXOR(ReversibleGate):
    def __init__(self, a, b, name = DEFAULT_COMPONENT_NAME):
        super().__init__(name)

        self.inputs = [a, b]

    def generateTruths(self, expected = True):
        if expected == True:
            return [
                Truth(False, True),
                Truth(True, False)
            ]
        else:
            return [
                Truth(False, False),
                Truth(True, True)
            ]

class RNOT(ReversibleGate):
    def __init__(self, a, name = DEFAULT_COMPONENT_NAME):
        super().__init__(name)

        self.inputs = [a]

    def generateTruths(self, expected = True):
        return [Truth(not expected)]

def printPermutationDiagram(permutations, depth = 0):
    indent = "    " * (depth * 2)

    for i in range(0, len(permutations)):
        print(indent + "Permutation {cycle}: [{component}] {name} = {value}".format(
            cycle = i + 1,
            component = type(permutations[i].reference).__name__,
            name = permutations[i].reference.name,
            value = permutations[i].value
        ))

        for j in range(0, len(permutations[i].inputPermutations)):
            print(indent + "    Input {input}:".format(input = j + 1))
            printPermutationDiagram(permutations[i].inputPermutations[j], depth + 1)

def _normaliseDict(oldDict):
    newDict = {}

    for key in sorted(oldDict):
        newDict[key] = oldDict[key]

    return newDict

def _dedupeInputTable(a):
    b = []

    for i in a:
        if i not in b:
            b.append(_normaliseDict(i))

    return b

def inputPermutationsToInputTable(inputPermutations):
    inputTable = [{}]
    shouldDupeLastItem = False

    for i in range(0, len(inputPermutations)):
        if len(inputPermutations[i]) == 1 and isinstance(inputPermutations[i][0].reference, Input):
            inputTable[-1][inputPermutations[i][0].reference.name] = inputPermutations[i][0].value

    for i in range(0, len(inputPermutations)):
        if len(inputPermutations[i]) == 1 and isinstance(inputPermutations[i][0].reference, Input):
            continue

        for permutation in inputPermutations[i]:
            localInputTable = inputPermutationsToInputTable(permutation.inputPermutations)

            for inputValues in localInputTable:
                if shouldDupeLastItem:
                    inputTable.append(deepcopy(inputTable[-1]))

                shouldDupeLastItem = True

                inputTable[-1] |= inputValues

    return _dedupeInputTable(inputTable)

def solve(root: Component, expected = True):
    fullInputTable = []
    permutations = root.generatePermutations(expected)

    for permutation in permutations:
        fullInputTable += inputPermutationsToInputTable(permutation.inputPermutations)

    return fullInputTable

def _intersect2(a, b):
    result = []

    for i in range(0, len(a)):
        for j in range(0, len(b)):
            if _normaliseDict(a[i]) == _normaliseDict(b[j]):
                result.append(a[i])

    return result

def intersect(*s):
    s = list(s)

    if len(s) > 1:
        a = s.pop(0)
        s[0] = _intersect2(a, s[0])

        return intersect(*s)

    return s[0]

def union(*s):
    result = []

    for permutation in s:
        for inputTable in permutation:
            if inputTable not in result:
                result.append(inputTable)

    return result