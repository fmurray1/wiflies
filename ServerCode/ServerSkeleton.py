import socket
import sys
#This function will read the port off of the command line
def readArgs():

    cmds = {'port':0} #this can be expanded as more commands are entered

    for i in range(len(sys.argv)):
        if(sys.argv[i] == '-p'):
            cmds['port'] = sys.argv[i+1]

    return cmds

#This function just creates a simple TCP listener that prints the data received
def servListen(cmds):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('',int(cmds['port'])))
    sock.listen()
    while True:
        data = b''
        con, addr = sock.accept()
        while True:
            new_data = con.recv(4096)
            data += new_data
            if len(new_data) == 0:
                break
        try:
            print(data.decode('utf-8'))
        except:
            print('ERROR: Data received was not UTF-8!\n')
        con.close()


if __name__ == '__main__':
    cmds = readArgs()
    if cmds['port'] == 0:
        print("ERROR: No port was passed!\n")
    else:
        print("DEBUG: Listening on port: "+str(cmds['port']))
        servListen(cmds)