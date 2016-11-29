# -*- coding: iso-latin-1 -*-

# Versione OOP di multi-read-write.py.
#
# Tutta la parte di sincronizzazione è ora nella classe Buffer.  Le
# funzioni reader e writer sono quindi molto più semplici.  Sono anche
# state eliminate varie variabili globali, ad esempio con l'uso di una
# classe DownCounter per controllare i cicli "infiniti" dei reader e
# dei writer.

import threading
import random
import time
import sys


# logging
DO_SLEEP = 1   

class ReadError(Exception):
    pass

def down(sem):
    sem.acquire()
    
def up(sem):
    sem.release()

print_sem = threading.Semaphore(1)

def show(s, file=sys.stdout):
    down(print_sem)
    file.write(s + "\n")
    up(print_sem)

def sleep_between(min, max):
    diff = max - min
    time.sleep(float(min))
    time.sleep(diff * random.random())

class Buffer:
    def __init__(self, size):

        self._size = size
        self._data = [None] * size
        self._read_pos = 0
        self._write_pos = 0
        self._sem_empty = threading.Semaphore(size)
        self._sem_full =  threading.Semaphore(0)
        self._sem_read_pos = threading.Semaphore(1)
        self._sem_write_pos = threading.Semaphore(1)

    def write(self, item, id, count):
        down(self._sem_empty)
        down(self._sem_write_pos)
        self._data[self._write_pos] = item
        self._write_pos = (self._write_pos + 1) % self._size
        show("writer %3d wrote %3d count: %3d" % (
            id, item, count))
        up(self._sem_write_pos)
        up(self._sem_full)

    def read(self, id, count):
        down(self._sem_full)
        down(self._sem_read_pos)
        item = self._data[self._read_pos]
        self._read_pos = (self._read_pos + 1) % self._size       
        show("reader %3d read  %3d count: %3d" % (
            id, item, count))
        up(self._sem_read_pos)
        up(self._sem_empty)
        return item
    
class CounterError(Exception):
    pass

class DownCounter:

    def __init__(self, count):

        self._count = count
        self._sem = threading.Semaphore(1)
        
    def next(self):
        down(self._sem)
        value = self._count
        if self._count >= 0:
            self._count -= 1
        up(self._sem)
        return value
        
def make_item():
    return random.randint(0,100)

def writer(id, buffer, counter, sleep_range):

    while True:
        count = counter.next()
        if count < 0:
            show("writer %3d leaving" % id)
            break
        item = make_item()
        sleep_between(*sleep_range)
        buffer.write(item, id, count)
        
def use_item(i):
    pass 
    
def reader(id, buffer, counter, sleep_range):

    while True:
        count = counter.next()
        if count < 0:
            show("writer %3d leaving" % id)
            break
        item = buffer.read(id, count)
        if item == None:
            raise ReadError()
        use_item(item)
        sleep_between(*sleep_range)

def main(items_count, buffer_size,
         readers_count, writers_count,
         readers_sleep_range, writers_sleep_range):

    buffer = Buffer(buffer_size)

    counter = DownCounter(items_count)
    rr = [threading.Thread(target=reader,
            args=(id, buffer, counter, readers_sleep_range))
            for id in range(readers_count)]
        
    counter = DownCounter(items_count)
    ww = [threading.Thread(target=writer,
            args=(id, buffer, counter, writers_sleep_range))
            for id in range(writers_count)]

    tt = rr + ww
    for t in tt: t.start()
    for t in tt: t.join()

def usage():
    print("""\
Usage: multi-read-write [-i|--items-count   items_count]
                        [-b|--buffer-size   buffer_size]
                        [-w|--writers-count writers_count]
                        [-r|--readers-count readers_count]
                        [-h|--help]
    """)

if __name__ == '__main__':

    items_count = 40
    buffer_size = 8
    readers_count = 2
    writers_count = 3
    readers_sleep_range = (0.4, 0.5)
    writers_sleep_range = (0.1, 0.8)
    
    from getopt import gnu_getopt as get_opt

    optlist, args = get_opt(
        sys.argv,
        "hi:b:w:r:", [
            "help",
            "item-count=",
            "buffer-size=",
            "writers-count=",
            "readers-count="])
    
    for k,v in optlist:
        if k in ["-h", "--help"]:
            usage()
            sys.exit(0)
        if k in ["-i", "--items-count"]:
            items_count = int(v)
        if k in ["-b", "--buffer-size"]:
            buffer_size = int(v)
        if k in ["-w", "--writers-count"]:
            writers_count = int(v)
        if k in ["-r", "--readers-count"]:
            readers_count = int(v)

    show("""
    multi-read-write
        items_count   %3d
        buffer_size   %3d
        readers_count %3d
        writers_count %3d
        """ % (
            items_count,
            buffer_size,
            readers_count,
            writers_count),
        sys.stderr)
                
    main(
        items_count, buffer_size,
        readers_count, writers_count,
        readers_sleep_range, writers_sleep_range)

