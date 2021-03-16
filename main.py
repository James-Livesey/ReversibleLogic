from copy import deepcopy

DEFAULT_COMPONENT_NAME = "(Unnamed)"

class ReversibleGate:
    def __init__(self, name = DEFAULT_COMPONENT_NAME):
        self.name = name
        self.inputs = []

    def generateTruths(self, expected = True):
        return [[expected]]

    def toGateValueRepresentations(self, expected = True):
        representations = []

        for truth in self.generateTruths(expected):
            representations.append(GateValueRepresentation(self, truth))

        return representations

    def solveChildren(self, expected = True):
        representations = self.toGateValueRepresentations(expected)

        for representation in representations:
            representation.inputRepresentations = [None] * len(self.inputs)

            for i in range(0, len(self.inputs)):
                representation.inputRepresentations[i] = self.inputs[i].solveChildren(representation.values[i])

        return representations

class Input:
    def __init__(self, name = DEFAULT_COMPONENT_NAME):
        self.name = name
        self.value = None

    def solveChildren(self, value):
        self.value = value

        return deepcopy(self)

class GateValueRepresentation:
    def __init__(self, gate, values = []):
        self.gate = gate
        self.inputRepresentations = []
        self.values = values

class RAND(ReversibleGate):
    def __init__(self, a, b, name = DEFAULT_COMPONENT_NAME):
        super().__init__(name)

        self.inputs = [a, b]

    def generateTruths(self, expected = True):
        if expected == True:
            return [
                [True, True]
            ]
        else:
            return [
                [False, False],
                [False, True],
                [True, False]
            ]

class ROR(ReversibleGate):
    def __init__(self, a, b, name = DEFAULT_COMPONENT_NAME):
        super().__init__(name)

        self.inputs = [a, b]

    def generateTruths(self, expected = True):
        if expected == True:
            return [
                [False, True],
                [True, False],
                [True, True]
            ]
        else:
            return [
                [False, False]
            ]

class RXOR(ReversibleGate):
    def __init__(self, a, b, name = DEFAULT_COMPONENT_NAME):
        super().__init__(name)

        self.inputs = [a, b]

    def generateTruths(self, expected = True):
        if expected == True:
            return [
                [False, True],
                [True, False]
            ]
        else:
            return [
                [False, False],
                [True, True]
            ]

class RNOT(ReversibleGate):
    def __init__(self, a, name = DEFAULT_COMPONENT_NAME):
        super().__init__(name)

        self.inputs = [a]

    def generateTruths(self, expected = True):
        return [[not expected]]

def traverseSolvedGateValueRepresentations(representations, depth = 0, scope = "(Root)"):
    indentation = "|   " * (depth + 1)
    humanReadableForm = ("|   " * depth) + "{scope} (\n".format(scope = scope)

    representationCollections = []
    representationGates = []

    for representationObject in representations:
        if isinstance(representationObject, Input):
            humanReadableForm += indentation + "{name} = {value}\n".format(name = representationObject.name, value = representationObject.value)
        else:
            for i in range(0, len(representationObject)):
                representationCollections.append(representationObject[i])
                representationGates.append(representationObject[i].gate)

    if len(representationCollections) > 0:
        for i in range(0, len(representationCollections)):
            humanReadableForm += indentation + "Permutation {}:\n".format(i + 1)
            humanReadableForm += traverseSolvedGateValueRepresentations(representationCollections[i].inputRepresentations, depth + 1,
                "{gate}: {name}".format(gate = type(representationGates[i]).__name__, name = representationGates[i].name)
            )

    return humanReadableForm + ("|   " * depth) + ")\n"

# gate = ROR(Input("A"), ROR(Input("B"), Input("C")))

S = RXOR(RXOR(Input("A"), Input("B")), Input("Cin"))
Cout = ROR(RAND(Input("Cin"), RXOR(Input("A"), Input("B"))), RAND(Input("A"), Input("B"), "Q"))

# print(traverseSolvedGateValueRepresentations([gate.solveChildren(True)]))

# print(traverseSolvedGateValueRepresentations([S.solveChildren(True)]))
# print(traverseSolvedGateValueRepresentations([Cout.solveChildren(True)]))