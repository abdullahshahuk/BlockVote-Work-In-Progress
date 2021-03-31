import socket
import datetime
from threading import Thread
from socketserver import ThreadingMixIn

TCP_IP = '0.0.0.0'
TCP_PORT = 5001
BUFFER_SIZE = 1024

# A blockchain node of sorts

class ClientThread(Thread):

    def __init__(self,ip,port,sock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        print (" New thread started for "+ip+":"+str(port))
        print (datetime.datetime.now())

    def run(self):
        with open('blockchain.txt', 'ab') as f:
            print ('file opened')
            while True:
                #print('receiving data...')
                data = self.sock.recv(BUFFER_SIZE)
                print('data=%s', (data))
                if not data:
                    f.close()
                    print ('file close()')
                    break
                # write data to a file
                f.write(data)
        
        self.sock.close()
        print('connection closed')

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))
threads = []

index = 0

while True:
    tcpsock.listen(5)
    print ("Waiting for incoming connections...")
    (conn, (ip,port)) = tcpsock.accept()
    print ('Got connection from ', (ip,port))
    newthread = ClientThread(ip,port,conn)
    print (index)
    newthread.start()
    threads.append(newthread)
    index = index + 1

# Currently redundant code, may be used for multithreading at a later date
for t in threads:
    t.join()
    