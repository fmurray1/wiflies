import socket
import sys
from enum import Enum

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

	
currentFly = 'C0FFEEBEA575'

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
    sock.bind(('',int(cmds['port'])))
    sock.listen(10)
    while True:
        data = b''
        con, addr = sock.accept()
        while True:
            data += con.recv(4096)
            if len(data) % 4096 != 0:
                break
        try:
            print(data.decode('utf-8'))
        except:
            print('ERROR: Data received was not UTF-8!\n')
        con.close()

		
def buildGraph(deviceDict, beaconDict, fliesDict):
	try:
		import matplotlib.pyplot as plt
		import networkx as nx
	except:
		raise
	
	G=nx.Graph()
	
	for device, strength in deviceDict.iteritems():
		G.add_edge(currentFly, device, weight=strength)
	
	for beacon, strength in beaconDict.iteritems():
		G.add_edge(currentFly, beacon, weight=strength)

	pos=nx.spring_layout(G)
	
	nx.draw_networkx_nodes(G,pos,node_size=700)
	
	nx.draw_networkx_edges(G,pos, width=6)
	
	nx.draw_networkx_labels(G,pos,font_size=20,font_family='sans-serif')
	
	plt.axis('off')
	
	plt.show()
					
					
	
	
def populatGraph(str):
	ls = str.split('\n')
	for s in ls:
		s = s.split(':')
		if "device" in s[DeviceData.TYPE]:
			deviceDict[s[DeviceData.MACADDRESS]] = s[DeviceData.RSSI]
		elif "beacon" in s:
			beaconDict[s[BeaconData.MACADDRESS]] = s[BeaconData.RSSI]
	buildGraph(deviceDict, beaconDict)


if __name__ == '__main__':
    cmds = readArgs()
    if cmds['port'] == 0:
        print("ERROR: No port was passed!\n")
    else:
        print("DEBUG: Listening on port: "+str(cmds['port']))
        servListen(cmds)