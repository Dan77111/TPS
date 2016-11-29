# -*- coding:utf-8 -*-

# Versione Python dell'omonimo esempio in C.  Il programma accetta una
# lista di nomi di file sulla linea di comando.  Per ciascun file crea
# un nuovo processo figlio per calcolarne la dimensione.  Nel processo
# figlio ciene eseguita la funzione write_count che, a seconda del
# valore della variabile globale EXEC, fa una exec di un eseguibile
# esterno oppure usa la funzione char_count.  La comunicazione tra
# padre e figlio avviene tramite pipe.  Siccome il padre lancia prima
# tutti i figli e poi li aspetta, serve una pipe per ciascun figlio.
# Inoltre si deve tener traccia della relazione figlio, file, pipe per
# cui uso un dizionario che ha come chiave il PID e come valore la
# pipe e il file.

import sys
import os

EXEC = 1

def char_count(filename):
    # BUG: read fallisce per file troppo grandi (es: mpa di un film!).
    with open(filename, "rb") as file:
        return len(file.read())

def write_count(filename):
    if EXEC:
        prog = "./char_count.py"
        os.execl(prog, prog, filename);
        sys.stderr.write("execl of %s on %s failed.\n" % (
            prog, filename))
    else:
        print(char_count(filename))

def read_count():
    return sys.stdin.readline().strip()

def main(files):

    out = dict()
    for f in files:

        p = os.pipe()
        pid = os.fork()
        
        if pid == 0:             # child
            
            os.dup2(p[1], 1)
            write_count(f)
            return 0
        else:                    # parent           
            out[pid] = (p, f)

    for f in files:

        pid, _ = os.wait()
        p,f = out[pid]
        os.dup2(p[0], 0)
        count = read_count()
        print ("%s %s" % (count, f))

    return 0

if __name__ == '__main__':

    args = sys.argv[1:]
    sys.exit(main(args))
    
