# -*- coding: iso-latin-1 -*-

import threading
import random
import time
import sys

OPTIONS = list()

class ReadError(Exception):
    pass

def down(sem):
    sem.acquire()
    
def up(sem):
    sem.release()

SEM_FULL = threading.Semaphore(0)
SEM_EMPTY = threading.Semaphore(1)
SHOW_SEM = threading.Semaphore(1)
DATA = 100
STOPPER = 666

def show(s):
    down(SHOW_SEM)
    sys.stderr.write("%s\n" % s)
    up(SHOW_SEM)

def make_item(item):
    show("Prod start %s" % str(item))
    time.sleep(item)
    show("Prod done  %s" % str(item))
    return item

def use_item(item):
    show("Cons start %s" % str(item))
    time.sleep(item)
    show("Cons done  %s" % str(item))
    
def reader():

    while 1:
        down(SEM_FULL)
        item = DATA
        if item == STOPPER:
            up(SEM_EMPTY)
            return
        use_item(item)
        up(SEM_EMPTY)

def writer(items):

    global DATA
    for item in items:
        down(SEM_EMPTY)
        if item != STOPPER:
            item = make_item(item)
        DATA = item
        up(SEM_FULL)

def main(args):

    args = args + [STOPPER]
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

if __name__ == '__main__':

    import sys
    args = sys.argv[1:]
    main(args)
