import socket

#This function just creates a simple TCP listener that prints the data received
def servListen():

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    sock.bind(('',30333))
    sock.listen()
    while True:
        data = b''
        con, addr = sock.accept()
        while True:
            data += con.recv(4096)
            if len(data) % 4096 != 0:
                break
        print(data)
        con.close()





if __name__ == '__main__':
    servListen()