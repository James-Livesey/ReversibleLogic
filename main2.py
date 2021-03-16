from typing import List
from copy import deepcopy

DEFAULT_COMPONENT_NAME = "(Unnamed)"

class Component:
    def __init__(self, name = DEFAULT_COMPONENT_NAME):
        self.name = name

class Truth:
    def __init__(self, *mappings: List[bool]):
        self.mappings = mappings

class ReversibleGate(Component):
    def __init__(self, name = DEFAULT_COMPONENT_NAME):
        self.name = name
        self.inputs = []

    def generateTruths(self, expected = True) -> List[Truth]:
        return [Truth(expected)]

class Input(Component):
    def __init__(self, name = DEFAULT_COMPONENT_NAME):
        super().__init__(name)

        self.name = name
        self.value = None

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

def _solveHelper(root: Component, expected = True, inputValues = {}, depth = 0, permutations = []):
    truths = root.generateTruths(expected)

    for truth in truths:
        for i in range(0, len(root.inputs)):
            if isinstance(root.inputs[i], Input):
                inputValues[root.inputs[i].name] = truth.mappings[i]
            else:
                inputValues.update(_solveHelper(root.inputs[i], truth.mappings[i], deepcopy(inputValues), depth + 1, permutations)["inputValues"])

        if depth == 0:
            permutations.append(deepcopy(inputValues))

    return {
        "inputValues": inputValues,
        "permutations": permutations
    }

def solve(root: Component, expected = True):
    return _solveHelper(root = root, expected = expected, permutations = [])["permutations"]

def _normaliseDict(oldDict):
    newDict = {}

    for key in sorted(oldDict):
        newDict[key] = oldDict[key]

    return newDict

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

S = RXOR(RXOR(Input("A"), Input("B")), Input("Cin"))
Cout = ROR(RAND(Input("Cin"), RXOR(Input("A"), Input("B"))), RAND(Input("A"), Input("B")))

permsS = solve(S, False)
permsCout = solve(Cout, True)

print("S:", permsS)
print("Cout:", permsCout)
print("Intersect:", intersect(permsS, permsCout))