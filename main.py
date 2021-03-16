from copy import deepcopy

class ReversibleGate:
    def __init__(self):
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
    def __init__(self, name = "Unnamed"):
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
    def __init__(self, a, b):
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
    def __init__(self, a, b):
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
    def __init__(self, a, b):
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
    def __init__(self, a):
        self.inputs = [a]

    def generateTruths(self, expected = True):
        return [[not expected]]

def traverseSolvedGateValueRepresentations(representations, indentation = 0):
    humanReadableForm = "("

    subrepresentations = []

    for representationObject in representations:
        if isinstance(representationObject, Input):
            humanReadableForm += "{name} = {value}; ".format(name = representationObject.name, value = representationObject.value)
        else:
            subrepresentations += representationObject[0].inputRepresentations

    if len(subrepresentations) > 0:
        humanReadableForm += traverseSolvedGateValueRepresentations(subrepresentations, indentation + 1)

    return humanReadableForm + ") "

gate = RXOR(RXOR(Input("A"), RXOR(RAND(Input("D"), Input("E")), RXOR(RAND(Input("F"), RNOT(Input("B"))), Input("G")))), Input("C"))

print(traverseSolvedGateValueRepresentations([gate.solveChildren(True)]))