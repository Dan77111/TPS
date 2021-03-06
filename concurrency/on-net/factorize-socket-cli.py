from factorize import factorize_naive
import socket

def server(port, max_queue=5):

    sock = socket.socket(socket.AF_INET,
                         socket.SOCK_STREAM)
    sock.bind( ("", port) )
    sock.listen(max_queue)

    while 1:
        conn, addr = sock.accept()
        try:
            print ("Got connection from %s" % str(addr))
            while 1:
                data = conn.recv(1024).strip()
                print("Server got: '%s'" % data)
                if not data:
                    break
                if data == "quit":
                    conn.close()
                    return
                data = factorize_naive(int(data))
                conn.send(repr(data))
        finally:
            conn.close()
            return

def client(ip, port):

    sock = socket.socket(socket.AF_INET,
                         socket.SOCK_STREAM)
    sock.connect( (ip, port) )
        
    try:
        while 1:
            data = raw_input("echo> ")
            sock.send(data)
            data = sock.recv(1024)
            print("Client got: '%s'" % data)
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
    
