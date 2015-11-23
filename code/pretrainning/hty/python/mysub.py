import subprocess

print subprocess.call("ls -l", shell=True)
print subprocess.check_call(['ls', '-l'])
child = subprocess.Popen(["ping", "-c", "5", "www.google.com"])
child.wait()
print "parent process"
print child.poll()
child.kill()
print child.poll()

child1 = subprocess.Popen(["ls", "-l"], stdout=subprocess.PIPE)
print child1.stdout.read()
child2 = subprocess.Popen(["grep", "0:0"], stdin=child1.stdout, stdout=subprocess.PIPE)
out = child2.communicate()
print out
