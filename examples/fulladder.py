import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Example starts below (code above is to bootstrap imports)

from rl import *

S = RXOR(RXOR(Input("A"), Input("B")), Input("Cin"))
Cout = ROR(RAND(Input("Cin"), RXOR(Input("A"), Input("B"))), RAND(Input("A"), Input("B")))

permsS = solve(S, False)
permsCout = solve(Cout, True)

print("S:", permsS)
print("Cout:", permsCout)
print("Intersect:", intersect(permsS, permsCout))