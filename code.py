def convertb(num,m):
	if num == 0:
		return 0
	s=""
	while num>0:
		s = str(num%m) + s
		num = num // m

	return int(s)


i = 8
while i > 0:
	line = str(input())

	if line == "0":
		break

	base, num, mod = line.split()
	base = int(base)
	num = int(num, base)
	mod = int(mod, base)

	if base==10:
		print(num%mod)
	else:
		print(convertb(num%mod, base))


