# -*- coding: iso-latin-1 -*-

import threading
import random
import time
import sys
import time

OPTIONS = list()

class ReadError(Exception):
    pass

def wait(sem):
    sem.acquire()
    
def signal(sem):
    sem.release()

SEM_FULL = threading.Semaphore(0)
SEM_EMPTY = threading.Semaphore(1)
SEM_SHOW = threading.Semaphore(1)
STOPPER = None

# "declaration". written before read elsewhere
DATA = None
TIME = None

def show(s):
    wait(SEM_SHOW)
    sys.stderr.write("%s\n" % s)
    signal(SEM_SHOW)

def log_data(prefix, item, old):
    show("%s %2d %6.2f -> %6.2f" % (
        prefix, item, old, time.time() - TIME))
        
def make_item(item):
    old = time.time() - TIME
    time.sleep(item)
    log_data("make:", item, old)
    return item

def use_item(item):
    old = time.time() - TIME
    time.sleep(item)
    log_data("use: ", item, old)
    
def reader():

    while 1:
        wait(SEM_FULL)
        item = DATA
        if item == STOPPER:
            signal(SEM_EMPTY)
            show("reader done")
            return
        signal(SEM_EMPTY)
        use_item(item)
    
def writer(items):

    show("writer start")
    global DATA
    global TIME
    TIME = time.time()
    for item in items:
        item = make_item(item)
        wait(SEM_EMPTY)
        DATA = item
        signal(SEM_FULL)
    wait(SEM_EMPTY)
    DATA = STOPPER
    signal(SEM_FULL)
    show("writer done")

def main(args):

    items = [int(s) for s in args]
    print (items)

    rt = threading.Thread(
        target=reader,
        args=())
    
    wt = threading.Thread(
        target=writer,
        args=(items,))

    wt.start()
    rt.start()
    wt.join()
    rt.join()

    sys.exit(0)
    
if __name__ == '__main__':

    import sys
    args = sys.argv[1:]
    main(args)
