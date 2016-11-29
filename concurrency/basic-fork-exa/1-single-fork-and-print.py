# -*- coding:utf-8 -*-

# Esempio super minimale di fork. Una sola fork, e sia il figlio che
# il padre non fanno altro che scrivere i due ID. Il padre non aspetta
# il figlio e quindi, se il figlio "ritarda" diventa uno 'zombie' e
# viene 'adottato' dal processo 'init', per cui il parent ID che
# stampa non è quello del padre originale. Le due opzioni -c e -p
# permettono di scegliere di quanto "ritardare" l'esecuzione della
# printf nel figlio e nel padre; il default è zero per entrambi.

import os
import time
import random
import sys
import argparse

def show(s):
    sys.stderr.write(s + "\n")
    
def go(child_sleep, parent_sleep):
    pid = os.fork()
    if pid == 0:

        time.sleep(child_sleep)
        show("child:  %d with parent: %d" % (
            os.getpid(), os.getppid()))
        sys.exit(0)        
    else:  
        time.sleep(parent_sleep)

def parse_args(args):

    parser = argparse.ArgumentParser()
    add = parser.add_argument("-c", "--child-sleep", help="Child max sleep time (seconds).", type=float, default=0.5)
    add = parser.add_argument("-p", "--parent-sleep", help="Parent max sleep time (seconds).", type=float, default=3.0)
    opt = parser.parse_args(args)
    return opt

def main(args):

    opt = parse_args(args)
    show ("Runner: %d" % os.getpid())
    for _ in range(5):
        go(random.random() * opt.child_sleep,
           random.random() * opt.parent_sleep)

if __name__ == "__main__":

    import sys
    main(sys.argv[1:])
