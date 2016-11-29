import sys
import threading
try:
    import queue           # Python 3.x
except:
    import Queue as queue  # Python 2,x
    
from char_count import char_count

def char_count_wrapper(file, queue):
    queue.put((file, char_count(file)))
    
def main(files):

    q = queue.Queue()
    tt = [threading.Thread(
        target=char_count_wrapper,
        args=(f, q))
        for f in files]

    for t in tt:
        t.start()

    for _ in files:
        f,c = q.get()
        print("%6d %s" % (c, f))

    return 0

if __name__ == "__main__":

    sys.exit(main(sys.argv[1:]))

