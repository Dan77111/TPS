from factorize import factorize_naive
import socket
import os

def make_nums(n):
    # Un metodo semplice per restituire una lista di N numeri dispari
    # "grandi".
    return [99999999 + i * 2 for i in range(n)]

def server(port, max_queue=5):

    sock = socket.socket(socket.AF_INET,
                         socket.SOCK_STREAM)
    sock.bind( ("", port) )
    sock.listen(max_queue)

    N = 999 
    nums = make_nums(N)
    block_size = 43
    blocks = [nums[i:i + block_size]
              for i in range(0, len(nums), block_size)]
    
    for block in blocks:
        conn, addr = sock.accept()
        print ("Got connection from %s" % str(addr))
        print ("Sending range %d-%d" % (block[0], block[-1]))
        conn.send(repr(block))
        data = conn.recv(1024)
        print (data)

def client(ip, port):

    sock = socket.socket(socket.AF_INET,
                         socket.SOCK_STREAM)
    sock.connect( (ip, port) )

    try:
        data = sock.recv(1024)
        if not data:
            return
        data = eval(data)
        print("Client %s\ngot: '%s'" % (os.getpid(), data))
        d = dict()
        for n in data:
            ff = factorize_naive(n)
            # print (ff)
            d.update({n: ff})
        sock.send(repr(d))
    finally:
        sock.close()

if __name__ == '__main__':

    import sys
    import random
    port = 5000 
    args = sys.argv[1:]
    if not args:
        sys.exit(1)
    if args[0] == "-s":
        server(port)
    if args[0] == "-c":
        if len(args) > 1:
            ip = args[1]
        else:
            ip = "127.0.0.1"
        client(ip, port)
    
