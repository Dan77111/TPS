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

    time.sleep(.5)
    return
    for _ in range(count):
        pid, status = os.wait()
        show("term: %d" % pid)
        
def main():
    show("Starting...")
    go(5, random.random(), random.random())
    show("...done.")
    
if __name__ == "__main__":
    main()
