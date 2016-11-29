#! /usr/bin/env python
# -*- coding: iso-latin-1 -*-
import sys

def make_ranges(base, top, count):

    # COUNT range contigui come divisione del range BASE, TOP.
    #
    # Calcola e restituisce una lista di COUNT coppie (b,t) che
    # definiscono dei range contigui e di uguale lunghezza
    # (eventualmente tranne l'ultimo) che coprono range(BASE, TOP).
    #
    # La "correzione" di size serve nel caso, frequente, in cui COUNT
    # non è multiplo esatto di top-base, nel qual caso si salterebbe
    # l'ultimo intervallo (più piccolo degli altri).
    
    assert top > base, (top, base)
    assert count > 0, count

    # Posso calcolare size e verificare se c'è resto in due
    # modi. divmod è più "elegante", risparmia qualche calcolo ma
    # costa una chiamata a funzione. Degustibus...
    
    if True:
        size = (top - base) // count
        assert size > 0, size
        if size * count < top - base:
            size += 1
    else:
        size, rest = divmod(top - base, count)
        assert size > 0, size
        if rest > 0:
            size += 1

    # Il calcolo si può fare in più modi. Con un for su count (ma non
    # viene molto bello), con un while (che rende più chiara la
    # terminazione) o con una list comprehension (ma non è un
    # granché).  Io preferisco il while!  Anche la "correzione" del
    # secondo termine dell'ultimo intervallo si può fare in più modi.
    # La posso fare, come qui, su tutti gli intervalli; per "omogeneo"
    # ma ovviamente sprecone.  Oppure lo posso fare dopo il ciclo, ma
    # viene un po' brutto.  Ovviamente si può anche usare map e delle
    # lamba :)
    
    rr = list()
    b = base
    t = 0
    while t < top:
        t  = min(b + size, top)
        rr.append( (b, t) )
        b += size
        
    return rr

    # bb = [base + i * size for i in range(count)]
    # rr = map(lambda b: (b, min(b + size, top)), bb)
    # return rr

    # return [(b, min(b+size, top))
    #         for b in [
    #                 base + i * size
    #                 for i in range(count)]]

def check_ranges(rr, base, top, count):

    # 1. il numero di elementi di rr deve essere uguale a quello
    # richiesto (count)
    #
    # 2. ciascun intervallo deve essere una tupla di due elementi
    #
    # 3. la somma di tutti gli intervalli deve essere uguale al
    # "range" richiesto (top-base)
    #
    # 4. la "base" del primo intervallo deve essere uguale alla base
    # del range richiesto.
    #
    # 5. il "top" dell'ultimo intervallo deve essere uguale al "top"
    # del range richiesto.
    #
    # 6. il "top" di un intervallo deve essere uguale al "base" del
    # successivo.
    
    assert len(rr) == count               # 1
    for r in rr:                          # 2
        assert len(r) == 2
    tot = sum([r[1] - r[0] for r in rr])
    assert tot == top - base              # 3
    assert rr[0][0] == base               # 4
    assert rr[-1][1] == top               # 5
    for i in range(len(rr)-1):            # 6
        assert rr[i][1] == rr[i+1][0]    
                
if __name__ == '__main__':

    args = sys.argv[1:]
    base = 2
    top = 38
    count = 5
    if len(args) == 3:
        base, top, count = map(int, args)

    for r in range(5):
        print
        
    print ("Testing: ", base, top, count)
    rr = make_ranges(base, top, count)
    for r in rr:
        print r
    check_ranges(rr, base, top, count)
        
    
