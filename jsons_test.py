import jsons
from dataclasses import dataclass
from typing import Optional


@dataclass
class Clazz:
    t: tuple[int, int, int]

    def __init__(self, t=(1,2,3)):
        self.t = t


p0 = Clazz()
jj = jsons.dumps(p0)
p1 = jsons.loads(jj, Clazz)
print(p0)
print(jj)
print(p1)
print(p0 == p1)
