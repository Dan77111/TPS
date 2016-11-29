import sys
import os

def char_count(filename):
    with open(filename, "rb") as file:
        return len(file.read())

def write_count(filename):
    print(char_count(filename))

def read_count():
    return sys.stdin.readline().strip()

def main(files):

    for f in files:

        tube = os.pipe()
        pid = os.fork()
        
        if pid == 0:             # child
            
            os.dup2(tube[1], 1)
            write_count(f)
            return
        else:                    # parent
            
            os.dup2(tube[0], 0)
            os.waitpid(pid, 0)
            count = read_count()
            print ("%s %s" % (count, f))

    return 0

if __name__ == '__main__':

    # test_char_count()
    
    args = sys.argv[1:]
    sys.exit(main(args))
    
