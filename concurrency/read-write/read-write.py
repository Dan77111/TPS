# -*- coding: iso-latin-1 -*-
import threading
import random
import time
import sys

OPTIONS = list()

class ReadError(Exception):
    pass

def down(sem):
    if OPTIONS["do_sync"]:
        sem.acquire()
    
def up(sem):
    if OPTIONS["do_sync"]:
        sem.release()

print_sem = threading.Semaphore(1)

def show(s):
    down(print_sem)
    sys.stderr.write("%s\n" % s)
    up(print_sem)

def sleep_between(min, max):
    diff = max - min
    time.sleep(float(min))
    time.sleep(diff * random.random())

def make_item():
    if options["do_sleep"]:
        sleep_between(*OPTIONS["writer_times"])
    return random.randint(0,100)

def use_item(i):
    if options["do_sleep"]:
        sleep_between(*OPTIONS["reader_times"])
    if not options["verbose"]:
        show("%3d" % i)
    
def split_time(string):
    ss = [s.strip() for s in string.split(":")]
    if len(ss) not in (1,2):
        raise Exception("Bad time string %s" % string)
    if len(ss) == 1:
        ss.append(ss[0])
    if not ss[0]:
        ss[0] = 0
    ff = map(float, ss)
    if ff[0] > ff[1]:
        raise Exception("Bad time string %s" % string)
    return ff

def reader(items_count, buffer, sem_empty, sem_full):

    size = len(buffer)
    for i in range(items_count):
        down(sem_full)
        p = i % size
        c = buffer[p]
        buffer[p] = -1   # for checking
        if OPTIONS["verbose"]:
            show("<  %3d at %d" % (
                c, p))
        if (c < 0):
            raise ReadError(
                "item %d at pos %d == %d" %
                (i, p, c))
        up(sem_empty)
        use_item(c)

def writer(items_count, buffer, sem_empty, sem_full):

    size = len(buffer)
    for i in range(items_count):
        down(sem_empty)
        p = i % size
        c = make_item()
        buffer[p] = c
        if OPTIONS["verbose"]:
            show(" > %3d at %d" % (
                c, p))
        up(sem_full)
        
def show_options(options):
        print("""\
running read-write with:
    do_sleep: %(do_sleep)d 
    do_sync: %(do_sync)s
    items_count: %(items_count)d 
    buffer_size: %(buffer_size)d 
    reader_times: %(reader_times)s 
    writer_times: %(writer_times)s 
    verbose: %(verbose)s\
""" % options)

def usage():
        print("""\
read-write [options]
options:
    -i items_count
    -b buffer_size
    -r reader_times
    -w writer_times
    -s do_sleep
    -y do_sync
    -v verbose
    -h help\
""")

def main(options):

    global OPTIONS
    OPTIONS = options

    if options["verbose"]:
        show_options(options)
        
    buffer_size = options["buffer_size"]
    items_count = options["items_count"]
    
    buffer = [-1] * buffer_size
    sem_empty = threading.Semaphore(buffer_size)
    sem_full = threading.Semaphore(0)

    rt = threading.Thread(
        target=reader,
        args=(items_count, buffer, sem_empty, sem_full))
    wt = threading.Thread(
        target=writer,
        args= (items_count, buffer, sem_empty, sem_full))

    wt.start()
    rt.start()
    wt.join()
    rt.join()
    
if __name__ == '__main__':

    import sys
    from getopt import gnu_getopt

    options = {
        "do_sleep" : 1,
        "do_sync" : 1,
        "items_count" : 40,
        "buffer_size" : 8,
        "reader_times" : (0.0, 0.1),
        "writer_times" : (0.1, 0.25),
        "verbose" : False,
        }
        
    optlist, args = gnu_getopt(sys.argv[1:], "i:b:r:w:s:y:vh")

    for o,a in optlist:
        if   o == "-i": options["items_count"] = int(a)
        elif o == "-b": options["buffer_size"] = int(a)
        elif o == "-r": options["reader_times"] = split_time(a)
        elif o == "-w": options["writer_times"] = split_time(a)
        elif o == "-s": options["do_sleep"] = int(a)
        elif o == "-y": options["do_sync"] = int(a)
        elif o == "-v": options["verbose"] = True
        elif o == "-h":
            usage()
            sys.exit()
            
    main(options)

