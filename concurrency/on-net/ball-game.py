# -*- coding: iso-latin-1 -*-

import sys
import os
import socket
import select
import multiprocessing as mp

# print ("Running Python %s" % sys.version)
# use input for both Python 2 and 3
try:                                      
    input = raw_input
except:
    pass

DEBUG = False

def pack(obj):
    # Serializza OBJ per la trasmissione via socket.  Funziona sia in
    # Python 2 che in Python 3.
    return repr(obj).encode()

def unpack(obj):
    # De-serializza OBJ per la trasmissione via socket.  Funziona sia
    # in Python 2 che in Python 3.
    return eval(obj.decode())

class ClientData(object):

    def __init__(self):

        self.pos = [0, 0]
    
class Server(object):

    def __init__(self, port=5000):

        self.port = port
        self.read_socks = list()
        self.main_sock = None
        self.next_id = 0
        self.data = dict()
        
    def serve_forever(self, max_queue=5):

        # Questa è la socket su cui accetto le connessioni.  max_queue è
        # il numero massimo di client che vengono mantenuti in attesa.
        # Qui non dovrei avere problemi perché appena un client si
        # connette gli viene creata un'altra socket.
        self.main_sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM)
        self.main_sock.bind( ("", self.port) )
        self.main_sock.listen(max_queue)

        self.read_socks.append(self.main_sock)

        while self.read_socks:

            rr, ww, ee = select.select(self.read_socks, [], [])

            for r in rr:

                if r == self.main_sock:

                    new_sock, addr = r.accept()
                    print ("Server: new client at %s" % str(addr))
                    
                    self.read_socks.append(new_sock)

                    data = r.recv(1024)       
                    data = unpack(data)       
                    cid = int(data)
                    self.data[self.next_id] = ClientData()
                    self.next_id += 1
                else:

                    data = r.recv(1024)       
                    data = unpack(data)       # "unpickle"
                    cid = int(data)
                    self.update_client(cid)
                    data = pack(self.data[cid])
                    r.send(data)
        self.main_sock.close()
        return res 

    def update_client(self, cid):

        x,y = self.data[cid].pos
        self.data[cid] = x+2, y+3
        
class Client(object):

    def __init__(self, ip, port):

        self.cid = None
        self.ip = ip
        self.port = port

    def run_forever(self):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect( (self.ip, self.port) )
        except Exception as e:
            print ("Client: server closed ... leaving")
            sys.exit(0)

        while 1:
            self.wait(1)
            data = sock.recv(1024)
            if not data:
                return       
            data = unpack(data)
            if self.cid is None:
                self.cid = int(data)
            print("Client %d got %s" % (self.cid, data.pos))
            
def run_server(port):
    server = Server(port)
    if DEBUG:
        pass
    server.serve_forever()

def run_client(ip, port):
    client = Client(ip, port)
    client.run_forever()
    
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
    
