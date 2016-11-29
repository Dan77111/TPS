# -*- coding:utf-8 -*-

# Esempio di fork. Un certo numero di fork, e sia il figlio che il
# padre non fanno altro che scrivere i due ID. Il padre aspetta i
# figli "tutti insieme" dopo le fork, in un loop in cui usa wait
# (generica). Quindi, anche se i figli "ritardano" non succede nulla
# di male!  Le due opzioni -c e -p permettono di scegliere di quanto
# "ritardare" l'esecuzione della printf nei figli e nel padre; il
# default è zero per tutti.


import os
import time
import random
import sys
import argparse

def show(s):
    sys.stderr.write(s + "\n")
    
def go(count, child_sleep, parent_sleep):

    for _ in range(count):
        pid = os.fork()
        if pid == 0:

            time.sleep(child_sleep)
            show("child:  %d parent: %d" % (
                os.getpid(), os.getppid()))
            sys.exit(0)

    return
    for _ in range(count):
        pid, status = os.wait()
        show("term: %d" % pid)

def parse_args(args):

    parser = argparse.ArgumentParser()
    add = parser.add_argument("-c", "--child-sleep", help="Child max sleep time (seconds).", type=float, default=0.0)
    add = parser.add_argument("-p", "--parent-sleep", help="Parent max sleep time (seconds).", type=float, default=0.0)
    opt = parser.parse_args(args)
    return opt

def main(args):

    opt = parse_args(args)
    show ("Runner: %d" % os.getpid())
    go(5,
       random.random() * opt.child_sleep,
        random.random() * opt.parent_sleep)
                
if __name__ == "__main__":

    import sys
    main(sys.argv[1:])
