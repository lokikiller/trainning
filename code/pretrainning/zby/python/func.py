def func():
    global x
    print "x is ", x
    x = 1

x = 3
func()
print x
