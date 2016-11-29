# -*- coding:iso-latin-1 -*-

# Nuova versione di ice-store, con un codice più pulito senza tracce
# della sua provenienza C.  Quindi niente variabili globali,
# simulazione più realistica (i clerk non spuntano dal nulla) etc.  In
# più aggiungo argomenti della linea di comando e logging.

import random                   # choice
import threading                # Semaphore Thread
import time                     # sleep
import os                       # write
import logging

def show(mess):
    os.write(1, mess + "\n")
    
def down(sem):
    sem.acquire()

def up(sem):
    sem.release()

acquire = wait = down
release = signal = up

class Inspection():

    # Questa classe, di cui viene creata una sola istanza, serve a
    # gestire la sincronizzazione tra il manager (unico) e i vari
    # camerieri. La classe contiene sia il dato relativo al risultato
    # dell'ispezione (passed) sia i due semafori per la
    # sincronizzazione (requested, finished) che il semaforo per il
    # controllo di accesso al manager (lock).
    
    def __init__(self):
        self.passed = False
        self.requested = threading.Semaphore(0)
        self.finished = threading.Semaphore(0)
        self.lock = threading.Semaphore(1)

class Line():

    # Questa classe, di cui viene creata una sola istanza, serve a
    # gestire non la sincronizzazione tra i vari clienti ed il
    # cassiere ma tra i vari clienti che si vogliono mettere in coda.
    # Infatti la sincronizzazione con il cassiere è implicita nel
    # fatto che c'è una coda (gestita con il vettore di semafori
    # CUSTOMERS).
    
    def __init__(self, customers_count):
        self.number = 0
        self.requested = threading.Semaphore(0)
        self.customers = [threading.Semaphore(0)] * customers_count
        self.lock = threading.Semaphore(1)

# manager   ----------------------------------------

def do_inspection(inspected_count, approved_rate):
    mess = "manager: inspection %d" % inspected_count
    show(mess)
    return random.choice(range(approved_rate + 1)) > 0
     
def manager(tot_cones, approved_rate, inspection):

    approved_count = 0
    inspected_count = 0
    while approved_count < tot_cones:
        
        wait(inspection.requested)        
        inspection.passed = do_inspection(inspected_count, approved_rate)
        inspected_count += 1
        if inspection.passed:
            approved_count += 1
        signal(inspection.finished)           

    time.sleep(1)
    mess = "manager leaves: %d approved %d rejected" % (
        approved_count, inspected_count - approved_count)
    show(mess)

# clerk   ----------------------------------------
        
def make_cone(clerk, cone, customer):
    mess = "clerk %2d: making cone %d for customer %d" % (
        clerk, cone, customer)
    show(mess)

def log_inspection(clerk, cone, customer, passed):
    mess = "clerk %2d: cone %d for customer %d %s" % (
        clerk, cone, customer, 
        ["REJECTED", "passed"][passed])
    show(mess)
    
def clerk(id, customer, cone, clerk_done, inspection):

    passed = False
    while not passed:
        make_cone(id, cone, customer)
        acquire(inspection.lock)       # enter critical region
        signal(inspection.requested)   # ask for inspection
        wait(inspection.finished)      # leave office
        passed = inspection.passed
        log_inspection(id, cone, customer, passed)
        release(inspection.lock)       # leave critical region
    signal(clerk_done)                 # signal customer

# customer   ----------------------------------------
    
def browse_flavours(id, cones_count):
    mess = "customer %d: asking for %d cones" % (
        id, cones_count)
    show(mess)
    
def walk_to_cashier(customer_id):
    mess = "customer %d: served and going to cashier" % (
        customer_id)
    show(mess)

CLERK_COUNT = 0                 # just for logging

def customer(id, cones_count, line, inspection):

    # Questo semaforo viene passato a ciascun clerk al momento della
    # creazione del thread e ciascun clerk fa un 'up' quando ha
    # finito, quindi customer può fare altrettanti 'down' per
    # aspettare che tutti abbiano finito.
    
    clerk_done = threading.Semaphore(0)

    browse_flavours(id, cones_count)

    global CLERK_COUNT
    for c in range(cones_count):          # "create" clerk
        t = threading.Thread(target=clerk,
                             args=(CLERK_COUNT + 1,
                                   id, c, clerk_done, inspection))
        t.start()
        CLERK_COUNT += 1
    for c in range(cones_count):          # wait for clerks
        wait(clerk_done)

    walk_to_cashier(id)
    acquire(line.lock)         # enter critical region
    num = line.number          # get ticket number
    line.number += 1
    release(line.lock)         # leave critical region
    signal(line.requested)     # wake up cashier
    wait(line.customers[num])  # wait in line

# cashier   ----------------------------------------
    
def check_out(i):
    mess = "cashier: customer %d paid" % i
    show(mess)

def cashier(customers_count, line):

    for i in range(customers_count):
        wait(line.requested)       # for customers to show up
        check_out(i)
        signal(line.customers[i])            

# main   ----------------------------------------
        
def ice_store(customers_count, max_cones_per_customer, approved_rate):

    # set up cones' data

    cones = [random.choice(range(1, max_cones_per_customer))
             for i in range(customers_count)]
    tot_cones = sum(cones)
    mess = "main: %d cones %s" % (tot_cones, str(cones))
    show(mess)

    inspection = Inspection()
    line = Line(customers_count)
    
    # create threads

    cts = [threading.Thread(target=customer,
                            args=(i,n, line, inspection))
           for i,n in enumerate(cones)]
    ct = threading.Thread(target=cashier,
                          args=(customers_count, line))
    mt = threading.Thread(target=manager,
                          args=(tot_cones, approved_rate, inspection))
    
    ct.start()                     # start threads
    mt.start()
    for t in cts:
        t.start()

    for t in cts:     # wait for threads to finish
        ct.join()
    mt.join()
    ct.join()

    return 0

def parse_args(args):

    import argparse

    parser = argparse.ArgumentParser(description='Ice store simulation.')
    add = parser.add_argument

    add("--customers_count", type=int, default=10,
        help="Number of customers buying ice cream cones.")
    add("--max-cones-per-customer", type=int, default=5,
        help="Max number of cones per customer.")
    add("--approved-rate", type=int, default=9,
        help="Number of approved cones per trashed cones.")

    return parser.parse_args(args)
    
def main(args):

    args = parse_args(args)
    ice_store(args.customers_count,
              args.max_cones_per_customer,
              args.approved_rate)

if __name__ == '__main__':

    import sys
    sys.exit(main(sys.argv[1:]))
