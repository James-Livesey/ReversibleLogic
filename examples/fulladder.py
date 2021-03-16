import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Example starts below (code above is to bootstrap imports)

from rl import *

S = RXOR(RXOR(Input("A"), Input("B")), Input("Cin"))
Cout = ROR(RAND(Input("Cin"), RXOR(Input("A"), Input("B"))), RAND(Input("A"), Input("B")))

permsS = solve(S, False)
permsCout = solve(Cout, False)

print("S:", permsS)
print("Cout:", permsCout)
print("Intersect:", intersect(permsS, permsCout))

################################################################################

# output = [True, False, True, False]

# def fullAdderFactory(id, lastCin):
#     return {
#         "S": RXOR(RXOR(Input("A" + id), Input("B" + id)), lastCin),
#         "Cout": ROR(RAND(lastCin, RXOR(Input("A" + id), Input("B" + id))), RAND(Input("A" + id), Input("B" + id)))
#     }

# S0 = fullAdderFactory("0", Input("Cin0"))
# S1 = fullAdderFactory("1", S0["Cout"])
# S2 = fullAdderFactory("2", S1["Cout"])
# S3 = fullAdderFactory("3", S2["Cout"])

# permsS0 = solve(S0["S"], output[0])
# permsS1 = solve(S1["S"], output[1])
# permsS2 = solve(S2["S"], output[2])
# permsS3 = solve(S3["S"], output[3])

# print(permsS0, permsS1, permsS2, permsS3)