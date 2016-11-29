# -*- coding:latin-1 -*-

# Esercizio sul problema producer/consumer, con un singolo producer,
# un singolo consumer e senza buffer, ovvero con una variabile globale
# su cui avviene il "passaggio" di un singolo "item".
#
# Ciò che voglio indagare sono i tempi di lavoro e di attesa dei due
# processi.  Una prima possibilità è ovviamente quelle di scrivere un
# programma concorrente e in qualche modo "stampare" i tempi che mi
# interessano.  Una seconda possibilità è fare tutto "gesso e lavagna"
# creando un schema che mostri lo sviluppo nel tempo dei due processi.
# Una terza possibilità è creare una tabella con cinque colonne che
# contengono rispettivamente, per ciascun item: il tempo di
# produzione/consumo, il momento di fine produzione, il momento di
# scrittura nella variabile globale, il momento di lettura della
# stessa e il momento di consumo.  Da questa tabella, confrontando i
# dati di varie colonne è possibile ricavare i tempi di lavoro e
# quelli di utilizzo della variabile globale.
#
# Questo programma, a partire dalla lista di tempi di produzione e
# consumo dei vari item, crea automaticamente la tabella e la lista
# dei "tempi".

# Esempio di output:
#
#   data
#   [2, 1, 4, 5, 1, 3, 3]
#   prod
#   2 1 4 5 1 3 -1 3 
#   (16, 17) 
#   wait
#   3 -1 9 -4 -1 2 -1 3
#   (3, 4) (13, 17) (17, 18) (20, 21) 
#   cons
#   -2 2 1 -2 4 -1 5 1 3 3 
#   (0, 2) (5, 7) (11, 12) 
#
#   |  t |  p |  s |  r |  c |  o |
#  -
#   |  2 |  2 |  2 |  2 |  4 |  0 |
#   |  1 |  3 |  3 |  4 |  5 |  4 |
#   |  4 |  7 |  7 |  7 | 11 |  5 |
#   |  5 | 12 | 12 | 12 | 17 | 11 |
#   |  1 | 13 | 13 | 17 | 18 | 17 |
#   |  3 | 16 | 17 | 18 | 21 | 18 |
#   |  3 | 20 | 20 | 21 | 24 | 21 |

def calc_table(tt):                 # tt: lista dei tempi (interi)
    rr = list()                     # "tabella" risultato
    s, r, c, o = [0] * 4
    for t in tt:                    # durata di prod/cons
        p = s + t                   # tempo di prod
        s = max(p, r)               # tempo di send
        r = max(s, c)               # tempo di receive
        c = r + t                   # tempo di cons
        rr.append( (t,p,s,r,c,o) )  # tutti in riga!
        o = c                       # valore precedente di cons
    return rr

def banner(string, tot_len=40):
    start = "%s " % string
    padding = "-" * (tot_len - len(start))
    print("%s%s-" % (start, padding))
           
def print_table(tt):
    banner("table -----------------------------")
    rr = calc_table(tt)
    b = ("|  t |  p |  s |  r |  c |  o |")
    print (b)
    print ("-" * len(b))
    for r in rr:
        ss = ["%2d" % i for i in r]
        s = " | ".join(ss)
        print ("| %s |"% s)

def producer(rr):                             # Dati relativi al producer
    banner("prod")

    # Stampa dei tempi
    for t,p,s,r,c,o in rr:
        print (t),
        # Il produttore è rimasto in attesa se il tempo (istante) di
        # "send" (scrittura nella variabile globale) è maggiore di
        # quello di "produzione".  Il tempo di attesa viene scritto
        # come numero negativo per distinguerlo da quello di lavoro.
        w = s - p
        if w:
            print (-w),
    print ("")

    # Stampa degli intervalli di attesa
    for t,p,s,r,c,o in rr:
        w = s - p
        if w:
            print (p, s),
    print ("")
    
def consumer(rr):                             # Dati relativi al consumer
    banner("cons")

    # Stampa dei tempi    
    for t,p,s,r,c,o in rr:
        # Il consumatore è rimasto in attesa se il tempo (istante) di
        # "read" (lettura nella variabile globale) è maggiore di
        # quello di "consumo" dell'item precedente (variabile o).  Il
        # tempo di attesa viene scritto come numero negativo per
        # distinguerlo da quello di lavoro.
        w = r - o
        if w:
            print -w,
        print (t),
    print ("")
    
    # Stampa degli intervalli di attesa
    for t,p,s,r,c,o in rr:
        w = r - o
        if w:
            print (o, r),
    print ("")

def buffer(rr):          # Dati relativi al "buffer" (variabile globale)
    banner("buffer")

    # Stampa dei tempi
    a = 0
    for t,p,s,r,c,o in rr:
        # Il buffer è "pieno", quando il tempo (istante) di lettura è
        # maggiore di quello di scrittura.  Il tempo di "buffer pieno"
        # viene scritto come numero negativo per distinguerlo da
        # quello di "buffer libero".
        w = r-s
        if w:
            if s-a:
                print (s-a),
            print (-w),
            a = r
    print (t)

    # Stampa degli intervalli di "buffer pieno"
    for t,p,s,r,c,o in rr:
        w = r-s
        if w:
            print (s,r),
    print ("")

def main(tt):
    rr = calc_table(tt)
    print ("")
    print ("data")
    print (tt)
    producer(rr)
    buffer(rr)
    consumer(rr)
    print ("")
    print_table(tt)
        
if __name__ == '__main__':

    import sys
    args = sys.argv[1:]
    if not args:
        tt = [2,1,4,5,1,3,3]
    else:
        tt = map(int, args)

    main(tt)
    

# Local Variables:
# comment-fill-column: 50
# End:
