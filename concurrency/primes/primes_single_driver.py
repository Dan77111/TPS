#! /usr/bin/env python
# -*- coding: iso-latin-1 -*-
import sys
import os
from primes_single import is_prime
from ranges import make_ranges
import multiprocessing as mp

DEBUG = 1

def log(message):
    if DEBUG:
        sys.stderr.write(str(message) + "\n")
        
def primes_in_range(min, max):
    return [n for n in range(min, max)
            if is_prime(n)]

def fun(id, min, max, queue):
    queue.put((id, primes_in_range(min, max)))

def usage():
    prog = sys.argv[0]
    print ("Usage: %s up-to proc-count" % prog)

if __name__ == '__main__':

    import os
    
    args = sys.argv[1:]
    if len(args) != 2:
        usage()
        sys.exit(1)

    try:
        top, proc_count = map(int, args)
    except ValueError:
        log("Bad args %s" % args)
        usage()
        sys.exit(1)

    log("Searching for primes up to %d with %d processes" % (
        top, proc_count))

    queue = mp.Queue()
    rr = make_ranges(0, top, proc_count)
    
    pp = [mp.Process(target=fun, args=(i, b, t, queue))
            for i, (b,t) in enumerate(rr)]

    for p in pp: p.start()
    # os.system("ps ax | grep python | grep Z+ 1>&2")
    for p in pp: p.join()

    all = list()
    for p in pp:
        out = queue.get_nowait()
        log(out)
        all.extend(out[1])

    all.sort()
    print (" ".join(map(str,all)))
        
    
