mtuple = (123, 'xyz', 45.67)
i = iter(mtuple)

print i.next()

print i.next()

print i.next()

# print i.next()

rows = [1, 2, 7, 8]
def cols():
    yield 56
    yield 2
    yield 1

x_product_pairs = ((i, j) for i in rows for j in cols())

for pair in x_product_pairs:
    print pair


f = open('/proc/diskstats', 'r')
longest = max(len(x.strip()) for x in f)
f.close()
print longest

