import ast
import jsons

import Substrate


p0 = Substrate.SubstrateParameters()
jj = jsons.dumps(p0)
p1 = jsons.loads(jj, Substrate.SubstrateParameters)
print(p0)
print(jj)
print(p1)
print(p0 == p1)

rr = repr(p0)
print(rr)
p2 = ast.literal_eval(rr)
print(p2)
print(p0==p2)
