# -*- coding: utf-8 -*-

import threading
import random
import time
import sys
import multiprocessing
import Queue

DO_SLEEP = 1

def down(sem): sem.acquire()
def up(sem): sem.release()
print_sem = threading.Semaphore(1)
def show(s, file=sys.stdout):
    down(print_sem)
    file.write(s + "\n")
    up(print_sem)

def sleep_between(min, max):
    diff = max - min
    time.sleep(float(min))
    time.sleep(diff * random.random())

def make_item():
    if DO_SLEEP: sleep_between(0.1, 0.2)
    return random.randint(0, 100)

def use_item(i):
    if DO_SLEEP: sleep_between(0.2, 0.3)

def writer(id, queue, counter):
    while 1:
        try:
            c = counter.get_nowait()
        except Queue.Empty:
            show("writer %3d leaving" % (id))
            break
        i = make_item()
        queue.put(c)

def reader(id, queue):
    while 1:
        c = queue.get()
        if c is None:
            show("reader %3d leaving" % (id))
            break
        show("reader %3d got %3d" % (id, c))
        use_item(c)

def main(items_count, readers_count, writers_count):

    counter = multiprocessing.Queue(items_count)
    queue = multiprocessing.Queue()

    for i in range(items_count):
        counter.put(i)

    rr = [threading.Thread(target=reader,
            args=(id, queue))
            for id in range(readers_count)]
    ww = [threading.Thread(target=writer,
            args=(id, queue, counter))
            for id in range(writers_count)]

    for w in ww: w.start()
    for r in rr: r.start()
    for w in ww: w.join()
    for r in rr:
        queue.put(None)
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

    for k, v in optlist:
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
