# 2-4 a
ustr = raw_input("Enter your strings:")
print ustr

# 2-4 b
uint = raw_input("Enter your int:")
print int(uint) * 2

# 2-5
a = 0
while a < 11:
    print a
    a += 1

for i in range(0, 11, 1):
    print i

# 2-6
var = int(raw_input("Enter your int:"))
if var == 0:
    print "zero"
elif var < 0:
    print "ne"
else:
    print "po"

# 2-7
var = raw_input("Enter your str:")
i = 0
slen = len(var)
while i < slen:
    print var[i]
    i += 1

for c in var:
    print c

# 2-9
sum = 0
for i in range(5):
    sum += float(raw_input("Enter you int"))
print sum / 5
