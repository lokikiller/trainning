import subprocess

ip = raw_input("Enter your host ip:")

def testCommunicate():
    child1 = subprocess.Popen(["ping", ip, "-c", "1"], stdout=subprocess.PIPE)
    child2 = subprocess.Popen(["grep", "ttl="], stdin=child1.stdout, stdout=subprocess.PIPE)
    out = child2.communicate()
    return out[0]


def main():
    while True:
        if testCommunicate():
            for i in range(100):
                print '\a'
            break


if __name__ == '__main__':
    main()
