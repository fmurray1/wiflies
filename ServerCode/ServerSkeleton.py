import socket
import sys
from enum import Enum
import matplotlib.pyplot as plt
import networkx as nx
from sets import Set

class BeaconData(Enum):
    TYPE = 0
    BSSID = 1
    MACADDRESS = 2
    CHANNEL = 3
    RSSI = 4
    
class DeviceData(Enum):
    TYPE = 0
    MACADDRESS = 1
    BSSID = 2
    DESTMAC = 3
    CHANNEL = 4
    RSSI = 5

G = nx.Graph()
WiFlyNodes = Set()
currentFly = 'C0FFEEBEA575'
deviceDict = {}
beaconDict = {}
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
    sock.listen(10)
    while True:
        data = b''
        con, addr = sock.accept()
        while True:
            new_data = con.recv(4096)
            data += new_data
            if len(new_data) == 0:
                break
        try:
            print("got data")
            populateGraph(data.decode('utf-8'))
        except Exception as e:
            print(e)
        con.close()

        
def buildGraph(deviceDict, beaconDict, currentFly):
    
    print('buildGraph')
    
    WiFlyNodes.update(currentFly)
    for device, strength in deviceDict.iteritems():
        G.add_edge(currentFly, device, weight=strength)
    
    for beacon, strength in beaconDict.iteritems():
        G.add_edge(currentFly, beacon, weight=strength)
        
    print(G.edges())

    pos=nx.spring_layout(G)
    
    nx.draw_networkx_nodes(G,pos,node_size=25, node_color="g")
    nx.draw_networkx_nodes(G,pos,node_list=WiFlyNodes, node_color="b", node_size=150)
   
    nx.draw_networkx_edges(G,pos, width=.5)
    
    nx.draw_networkx_labels(G,pos,font_size=6,font_family='sans-serif')
    
    plt.axis('off')
    plt.draw()
    plt.pause(0.05)
                   
def populateGraph(str):
    print('populateGraph')
    ls = str.split('\n')
    currentFly = ls[0]
    currentFly = currentFly.replace(':','').lower()
    print('currentFly: {}'.format(currentFly))
    for s in ls[1:]:
        s = s.strip().split(':')
        print(s)
        if len(s) >= 4:
            if "DEVICE" in s[DeviceData.TYPE]:
                deviceDict[s[DeviceData.MACADDRESS]] = s[DeviceData.RSSI]
            elif "BEACON" in s:
                beaconDict[s[BeaconData.MACADDRESS]] = s[BeaconData.RSSI]
    print(deviceDict)
    print(beaconDict)
    buildGraph(deviceDict, beaconDict, currentFly)


if __name__ == '__main__':
    """
    test_dict = {'a':-70, 'b':-40}
    test_beacon = {}
    buildGraph(test_dict, test_beacon)
    """
    cmds = readArgs()
    if cmds['port'] == 0:
        print("ERROR: No port was passed!\n")
    else:
        print("DEBUG: Listening on port: "+str(cmds['port']))
        plt.ion()
        plt.show()
        servListen(cmds)