y = 10
x = -11
x = 0 if x < y > -x else "not"
print(x)

func = lambda x: 0 if x <= y >= -y else True

v1 = func(10); v2 = func(12)
print(v1, v2)

print(func(10))

data = "b1x532y495"
verdier = list(map(int, data[1:].replace('x', ' ').replace('y', ' ').split()))
#verdier[0], verdier[1] = int(verdier[0]) - 512, int(verdier[1]) - 512
verdier = [x - 512 for x in verdier[-2:]]

#x = 0 if abs(10) < 20 else "wow"
print(verdier)
#x_verdier, y_verdi = [0 if abs(x) < 20 else x for x in verdier[-2:]]
#print(x_verdier, y_verdi)
#print(verdier[:2])
x_verdi, y_verdi, b_verdi = [0 if abs(x) <= 20 else x for x in verdier] + [int(data[1:].split('x')[0])]
print(x_verdi, y_verdi, b_verdi)


#print(verdier)
#print(data[1:].split('x')[0])