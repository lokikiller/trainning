from datetime import *
import time

print 'date.max: ', date.max
print 'date.min: ', date.min
print 'date.today()', date.today()
print 'date.fromtimestamp()', date.fromtimestamp(time.time())

now = date(2010, 04, 06)
tomorrow = now.replace(day=07)
print 'now', now, 'tomorrow', tomorrow
print 'timetuple():', now.timetuple()
print 'weekday():', now.weekday()
