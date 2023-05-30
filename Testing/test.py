y = 10
x = -11
x = 0 if x < y > -x else "not"
print(x)

func = lambda x: 0 if x <= y >= -y else True

v1 = func(10); v2 = func(12)
print(v1, v2)

print(func(10))