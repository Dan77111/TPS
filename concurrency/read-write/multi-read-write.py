# -*- coding: iso-latin-1 -*-

# Classico esempio di lettori (readers) e scrittori (writers)
# multipli, che condividono un buffer di lunghezza finita,
# implementato con una lista gestita come un buffer circolare.
#
# Ci sono varie sincronizzazioni, la prima è relativa al buffer ed
# utilizza quattro semafori di semafori (sem_empty, sem_full e due
# sem_pos, uno per i reader e l'altra per i writer) e due variabili
# globali WRITE_POS e READ_POS.
#
# sem_empty indica il numero di celle vuote nel buffer, sem_full
# indica il numero di quelle piene. Su sem_empty i writer fanno una
# down (aspettano di avere del posto per scrivere) mentre i reader
# fanno una up (quando estraggono un dato liberando quindi una cella).
# Analogamente, su sem_full i reader fanno una down (aspettano che ci
# sia qualcosa da leggere) mentre i writer fanno una up (appena hanno
# riempito una nuova cella).
#
# WRITE_POS indica la posizione (indice della lista) della prima cella
# libera per scrivere, READ_POS indica la posizione della prima cella
# non ancora letta. Ovviamente queste variabili sono lette e scritte
# rispettivamente da writer e reader, ma siccome ci sono più writer e
# più reader servono dei semafori per garantire l'accesso esclusivo
# alle due variabili.

import threading
import random
import time
import sys

# sync
WRITE_POS = 0                 # where to write to
READ_POS = 0                  # where to read from
buffer = None                 # circular buffer

# logging
WRITE_LEFT = 0 # number of items still to be written
READ_LEFT = 0  # number of items still to be read
DO_SLEEP = 1   

class ReadError(Exception):
    pass

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
    return random.randint(0,100)

def use_item(i):
    if DO_SLEEP: sleep_between(0.5, 0.6)
    
def writer(id, sem_empty, sem_full, sem_pos):

    global WRITE_POS
    global WRITE_LEFT
    
    size = len(buffer)
    while True:
        down(sem_empty)
        down(sem_pos)
        if WRITE_LEFT == 0:
            show("writer %3d leaving" % id)
            up(sem_pos)
            up(sem_full)
            break
        WRITE_LEFT -= 1
        pos = WRITE_POS
        WRITE_POS = (WRITE_POS + 1) % size
        c = make_item()
        up(sem_pos)
        show("writer %3d writing %3d at %3d count: %d" % (
            id, c, pos, WRITE_LEFT))
        buffer[pos] = c
        up(sem_full)
        
def reader(id, sem_empty, sem_full, sem_pos):

    global READ_POS
    global READ_LEFT
    
    size = len(buffer)
    while True:
        down(sem_full)
        down(sem_pos)
        if READ_LEFT == 0:
            show("reader %3d leaving" % id)
            up(sem_pos)
            up(sem_empty)
            break
        READ_LEFT -= 1
        pos = READ_POS
        READ_POS = (READ_POS + 1) % size
        c = buffer[pos]
        show("reader %3d read    %3d at %3d count: %d" % (
            id, c, pos, READ_LEFT))
        buffer[pos] = -1   # for checking
        if (c < 0):
            exit(1)
            raise ReadError()
        up(sem_pos)
        up(sem_empty)
        use_item(c)

def main(items_count, buffer_size,
         readers_count, writers_count):

    global WRITE_LEFT
    global READ_LEFT
    global DO_SLEEP
    global WRITE_POS 
    global READ_POS 
    global buffer

    WRITE_LEFT = items_count
    READ_LEFT  = items_count
    DO_SLEEP = 1
    WRITE_POS = 0
    READ_POS = 0
    
    buffer = [-1] * buffer_size
    sem_empty = threading.Semaphore(buffer_size)
    sem_full = threading.Semaphore(0)
    sem_reader = threading.Semaphore(1)
    sem_writer = threading.Semaphore(1)
    
    rr = [threading.Thread(target=reader,
            args=(id, 
                  sem_empty, sem_full, sem_reader))
            for id in range(readers_count)]
    ww = [threading.Thread(target=writer,
            args=(id, 
                  sem_empty, sem_full, sem_writer))
            for id in range(writers_count)]

    for r in rr: r.start()
    for w in ww: w.start()
    for r in rr: r.join()
    for w in ww: w.join()

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
    writers_count = 3
    readers_count = 2

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
        writers_count %3d
        readers_count %3d
        """ % (
            items_count,
            buffer_size,
            writers_count,
            readers_count),
        sys.stderr)
                
    main(items_count, buffer_size,
         readers_count, writers_count)

