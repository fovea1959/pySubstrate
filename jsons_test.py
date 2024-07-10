import jsons


class T:
    t_field: tuple[int]

t = T()
t.t_field = (255, 255, 255)
s = jsons.dumps(t)
print(s)