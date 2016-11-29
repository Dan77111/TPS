# -*- coding: iso-latin-1 -*-

# Esempio di calcolo (fattorizzazione) distribuito tra più client che
# interagiscono con un server centrare che distribuisce il lavoro (fan
# out) e raccoglie i risultati (fan in).  La comunicazione avviene via
# socket, senza usare nessuna libreria di alto livello.  I dati (liste
# all'andata e dizionari al ritorno) vengono trasformati in stringhe
# usando "repr" e poi riconvertiti con "eval".  Forse avrei potuto
# anche scomodare pickle, ma per dati così semplici non è necessario.

# Un istanza di questo programma, eseguito con l'opzione "-s" fa da
# server, altre istanze, eseguite con l'opzione "-c" (e con eventuale
# argomento PORT) fanno da client e si connettono al server.  Il
# server genera una lista di numeri (dispari e grandi) e la divide in
# un certo numero di "sottoliste" (chunks) di una certa dimensione.
# Ogni client che si connette riceve un "chunk" di numeri da
# fattorizzare, li fattorizza, mette il risultato in un dizionario in
# cui il numero da fattorizzare è la chiave e la lista dei fattori è
# il valore e li spedisce al server.  Il server raccoglie i vari
# dizionari e li "raccoglie" in un unico dizionario.

import sys
import os
import socket
import select
import multiprocessing as mp
from factorize import factorize_naive

# print ("Running Python %s" % sys.version)
# use input for both Python 2 and 3
try:                                      
    input = raw_input
except:
    pass

DEBUG = False

def make_nums(base, count):
    # Count numeri dispari da BASE in su.
    assert base % 2 == 1
    return [base + i * 2 for i in range(count)]

def pack(obj):
    # Serializza OBJ per la trasmissione via socket.  Funziona sia in
    # Python 2 che in Python 3.
    return repr(obj).encode()

def unpack(obj):
    # De-serializza OBJ per la trasmissione via socket.  Funziona sia
    # in Python 2 che in Python 3.
    return eval(obj.decode())

def server(port, max_queue=5):

    # Questa è la socket su cui accetto le connessioni.  max_queue è
    # il numero massimo di client che vengono mantenuti in attesa.
    # Qui non dovrei avere problemi perché appena un client si
    # connette gli viene creata un'altra socket.
    main_sock = socket.socket(socket.AF_INET,
                            socket.SOCK_STREAM)
    main_sock.bind( ("", port) )
    main_sock.listen(max_queue)

    # dizionario dei risultati
    res = dict()
 
    # lista dei num_count numeri da fattorizzare, divisa poi in
    # blocchi di BLOCK_SIZE elementi.
    num_count = 999 
    nums = make_nums(99999999999, num_count)
    block_size = 43
    blocks = [nums[i:i + block_size]
              for i in range(0, len(nums), block_size)]

    # READ_SOCKS sono le  socket da cui "leggo". All'inizio c'è solo
    # MAIN_SOCK, poi si aggiungono quelle aperte per ciascuna
    # connessione.
    read_socks = [main_sock]
    
    while read_socks:
        
        # socket pronte per leggere, scrivere, ...
        #
        # select "controlla" le tre liste di socket fornite come
        # parametri e restituisce le tre "sottoliste" che hanno dati
        # da cui leggere (RR), che sono in attesa di dati (WW) o che
        # hanno generato errori (EE).  A me interessano solo quelle
        # "leggibili" in quanto la scrittura la faccio direttamente
        # subito dopo la connessione.
        
        rr, ww, ee = select.select(read_socks, [], [])
        
        for r in rr:

            # Le connessioni in lettura possono essere di due "tipi":
            # o sono la socket principale MAIN_SOCK su cui aspetto le
            # connessioni iniziali dei client oppure quelle dei client
            # già connessi da cui aspetto i risultati.
            
            if r == main_sock:
                
                # Connessione iniziale di un client, creo una nuova
                # socket e la aggiungo alle socket da cui leggere.
                new_sock, addr = r.accept()
                print ("Server: new client at %s" % str(addr))
                read_socks.append(new_sock)

                # Gli mando il primo blocco e lo cancello.
                p = pack(blocks[0])                  # "pickle"
                new_sock.send(p)                     # send
                del blocks[0]                        # done with it!

                # Se non ci sono più blocchi il server ha finito.
                if not blocks:
                    print ("Server: done")
                    read_socks.remove(main_sock)
                    main_sock.close()
            else:
                # Connessione di un client specifico, da cui devo
                # leggere il risultato della fattorizzazione.
                
                data = r.recv(5024)       # BAD!!!
                data = unpack(data)         # "unpickle"
                res.update(data)          # append
                r.close()                 # bye
                read_socks.remove(r)      # done with it!
                print ("Server: client done")
    main_sock.close()
    return res 

def client(ip, port):

    # Creo una socket e provo a connettermi al server all'indirizzo IP
    # e porta PORT.
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect( (ip, port) )
    except Exception as e:
        print ("Client: server closed ... leaving")
        sys.exit(0)

    try:
        # Leggo la lista di numeri da fattorizzare, serializzata da
        # PACK e la de-serializzo con UNPACK.
        data = sock.recv(1024)
        if not data:
            return       
        data = unpack(data)         
        print("Client %s\ngot range: %d-%d" % (
            os.getpid(), data[0], data[-1]))

        # Calcolo i fattori, li metto nel dizionario come valori dei
        # numeri, serializzo tutto, lo mando al server e poi saluto e
        # vado.
        d = dict()
        for n in data:
            ff = factorize_naive(n)
            d.update({n: ff})                # dict via comprehension!
        sock.send(pack(d))                   # deserializzo
    finally:
        sock.close()

def check_res(res):
    # Controllo del risultato.  Calcolo il prodotto dei fattori e
    # controllo che sia uguale al numero originale.
    ok_bad = [0,0]
    for k,v in res.items():
        t = 1
        for n in v: t *= n
        c = (k == t)
        ok_bad[1-c] += 1
    return ok_bad

def run_server(port):
    res = server(port)
    if DEBUG:
        for k,v in res.items():
            print (k, 40 * "-")
            print (v)
    ok_bad = check_res(res)
    print ("OK: %d BAD: %d" % tuple(ok_bad))

def run_client(ip, port):
    cc = [mp.Process(target=client, args=(ip, port))
          for i in range(20)]
    for c in cc: c.start()
    for c in cc: c.join()
    
def usage():
    prog = os.path.basename(sys.argv[0])
    print ("Usage: %s [-s] [-c [port]]"% prog)
    
if __name__ == '__main__':

    import random
    port = 5000 
    args = sys.argv[1:]

    if not args:
        usage()
        sys.exit(1)
        
    if "-h" in args:
        usage()
        sys.exit(0)
        
    if args[0] == "-s":
        run_server(port)
        sys.exit(0)
        
    if args[0] == "-c":
        if len(args) > 1:
            ip = args[1]
        else:
            ip = "127.0.0.1"
        run_client(ip, port)
    
