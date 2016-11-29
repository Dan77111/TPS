# -*- coding: iso-latin-1 -*-

import threading
import random
import time
import sys
import Queue

DO_SLEEP = 1   

def down(sem): sem.acquire()
def up(sem): sem.release()  
print_sem = threading.Semaphore(1)
def show(s, file=sys.stdout):
#    down(print_sem)
    file.write(s + "\n")
#    up(print_sem)

class Counter:

    def __init__(self, value):
        self.value = value
        self.lock = threading.Lock()

    def next(self):
        with self.lock:
            v = self.value
            if v == 0:
                return 0
            self.value -= 1 
            return v

class LoggerQueue(Queue.Queue):

    def __init__(self, maxsize=0):
        Queue.Queue.__init__(self, maxsize)

    def _put(self, item):
        id = threading.current_thread().name 
        show("Writer %s put %s" % (id, item))
        self.queue.append(item)

    def _get(self):
        id = threading.current_thread().name
        item = self.queue.popleft()
        show("Reader %s got %s" % (id, item))
        return item

def sleep_between(min, max):
    diff = max - min
    time.sleep(float(min))
    time.sleep(diff * random.random())

def make_item():
    if DO_SLEEP: sleep_between(0.1, 0.2)
    return random.randint(0,100)

def use_item(i):
    if DO_SLEEP: sleep_between(0.5, 0.6)

def items_to_go():
    global ITEMS_COUNT
    down(ITEMS_COUNT_SEM)
    ITEMS_COUNT -= 1
    count = ITEMS_COUNT
    up(ITEMS_COUNT_SEM)
    return count
    
def writer(id, queue, counter):

    while 1:
        c = counter.next()
        if c == 0:
            show("writer %3d leaving" % (id))
            break
        i = make_item()
        queue.put(c, id)
        
def reader(id, queue):

    while 1:
        c = queue.get(id)
        if c is None:
            show("reader %3d leaving" % (id))
            break

def main(items_count, readers_count, writers_count):

    queue = LoggerQueue(items_count)
    counter = Counter(items_count)
    
    rr = [threading.Thread(target=reader, name="r_%0d" % id,
            args=(id, queue))
            for id in range(readers_count)]
    ww = [threading.Thread(target=writer, name="w_%0d" % id,
            args=(id, queue, counter))
            for id in range(writers_count)]

    for r in rr: r.start()
    for w in ww: w.start()
    for w in ww: w.join()
    for r in rr:
        queue.put(None, -1)
    for r in rr: r.join()

def usage():
    print("""\
Usage: multi-read-write [-i|--items-count   items_count]
                        [-w|--writers-count writers_count]
                        [-r|--readers-count readers_count]
                        [-h|--help]
    """)

if __name__ == '__main__':

    items_count = 40
    writers_count = 2
    readers_count = 5

    from getopt import gnu_getopt as get_opt

    optlist, args = get_opt(
        sys.argv,
        "hi:b:w:r:", [
            "help",
            "item-count=",
            "writers-count=",
            "readers-count="])
    
    for k,v in optlist:
        if k in ["-h", "--help"]:
            usage()
            sys.exit(0)
        if k in ["-i", "--items-count"]:
            items_count = int(v)
        if k in ["-w", "--writers-count"]:
            writers_count = int(v)
        if k in ["-r", "--readers-count"]:
            readers_count = int(v)

    show("""
    multi-read-write
        items_count   %3d
        writers_count %3d
        readers_count %3d
        """ % (
            items_count,
            writers_count,
            readers_count),
        sys.stderr)
                
    main(items_count, readers_count, writers_count)

