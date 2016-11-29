# -*- coding: iso-latin-1 -*-
import threading
import random
import time
import sys

OPTIONS = None              # Initialized in main!

class ReadError(Exception):
    pass

# I semafori usati qui sono degli oggetti Python con metodi acquire e
# release.  L'esempio originale è in C e usa funzioni down e up, e
# quindi mi "adeguo".  do_sync è l'opzione che indica se usare o no i
# semafori, così se do_sync è False si vede che "ci sono dei
# problemi".

def down(sem):
    if OPTIONS["do_sync"]:
        sem.acquire()
    
def up(sem):
    if OPTIONS["do_sync"]:
        sem.release()

# Per mostrare cosa sta succedendo, il codice è pieno di print
# chiamate dai vari thread. Per evitare che gli output dei vari thread
# si mescolino, uso un semaforo che garantisce l'accesso "un thread
# alla volta".
print_sem = threading.Semaphore(1)

def show(s):
    
    down(print_sem)
    sys.stderr.write("%s\n" % s)
    up(print_sem)

# Per simulare il "lavoro" di make_item e use_item introduco delle
# attese di durata variabile in modo casuale tra un minimo e un
# massimo.  I tempi di attesa sono specificati nelle opzioni
# reader_times e writer_times e si possono escludere settando a False
# l'opzione do_sleep.  Modificando i tempi di attesa e l'opzione
# do_sync si possono ottenere vari tipi di comportamenti "errati".

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

# split_time converte il valore dei tempi di attesa passati sulla riga
# di comando (che sono nel formato min:max) in una coppia di interi.

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
        
def usage():
        print("""\
read-write [options]
options:
    -i items_count    (es: -i 50)
    -b buffer_size    (es: -b  8)                   
    -r reader_times   (es: -r 0.2:1)                    
    -w writer_times   (es: -w .5:.8)
    -s do_sleep       (0 or 1)
    -y do_sync        (0 or 1)
    -v verbose        (no arg!)
    -h help           (no arg!)

Examples:
read-write -v
read-write -v -y 0
read-write -i 100 -y 0      \
""")

def main(options):

    global OPTIONS
    OPTIONS = options

    if options["verbose"]:
        show_options(options)
        
    buffer_size = options["buffer_size"]
    items_count = options["items_count"]

    # Il buffer viene inizializzato con -1, ed anche il reader, dopo
    # aver letto la cella corrente, ne setta il valore a -1. Il writer
    # scrive invece sempre valori non negativi.  In questo modo il
    # reader si può accorgere se (in assenza di sync o per errori nel
    # codice) ha letto un valore da una cella non ancora "scritta" (o
    # riscritta).
    
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

if __name__ == '__main__':

    import sys
    from getopt import gnu_getopt

    # Dizionario delle opzioni, con valori di default
    options = {
        "do_sleep" : 1,
        "do_sync" : 1,
        "items_count" : 40,
        "buffer_size" : 8,
        "reader_times" : (0.0, 0.1),
        "writer_times" : (0.1, 0.25),
        "verbose" : False,
        }

    # Parsing delle opzioni dalla linea di comando
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

