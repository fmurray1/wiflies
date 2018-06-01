import socket
import sys
import argparse
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
current_fly = 'C0FFEEBEA575'
device_dict = {}
beacon_dict = {}


# This function will read the port off of the command line
def read_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('port', help='The port for the serer to listen on.')

    return parser.parse_args()


# This function just creates a simple TCP listener that prints the data received
def server_listen(args):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', int(args.port)))
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
            populate_graph(data.decode('utf-8'))
        except Exception as e:
            print(e)
        con.close()

        
def build_graph(device_dict, beacon_dict, fly):
    
    print('buildGraph')

    WiFlyNodes.add(fly)

    for device, strength in device_dict.iteritems():
        G.add_edge(current_fly, device, weight=strength)
    
    for beacon, strength in beacon_dict.iteritems():
        G.add_edge(current_fly, beacon, weight=strength)

    print('Wiflies: {}'.format(WiFlyNodes))

    unknown_nodes = Set(device_dict.keys()+beacon_dict.keys()).difference(WiFlyNodes)

    print('Unknown: {}'.format(unknown_nodes))

    print(G.edges())

    pos = nx.spring_layout(G)
    
    nx.draw_networkx_nodes(G, pos, nodelist=unknown_nodes, node_size=25, node_color="green")
    nx.draw_networkx_nodes(G, pos, nodelist=WiFlyNodes, node_color="blue", node_size=150)
   
    nx.draw_networkx_edges(G, pos, width=.5)
    
    nx.draw_networkx_labels(G, pos, font_size=6, font_family='sans-serif')
    
    plt.axis('off')
    plt.draw()
    plt.pause(50)

  
def populate_graph(str):
    print('populateGraph')
    ls = str.split('\n')
    global current_fly
    current_fly = ls[0].replace(':', '').lower()
    print('current_fly: {}'.format(current_fly))
    for s in ls[1:]:
        s = s.strip().split(':')
        print(s)
        if len(s) >= 4:
            if "DEVICE" in s[DeviceData.TYPE]:
                device_dict[s[DeviceData.MACADDRESS]] = s[DeviceData.RSSI]
            elif "BEACON" in s:
                beacon_dict[s[BeaconData.MACADDRESS]] = s[BeaconData.RSSI]
    print(device_dict)
    print(beacon_dict)
    build_graph(device_dict, beacon_dict, current_fly)


if __name__ == '__main__':
    """
    global current_fly
    test_dict = {'a': -70, 'b': -40, 'c': -50, 'd': -99}
    test_beacon = {'e': -55, 'f': -85}
    build_graph(test_dict, test_beacon, current_fly)
    """
    """
    import random
    test_str = current_fly + '\n'
    for c in ['a', 'b', 'c', 'd']:

        temp = ['0'] * 6
        temp[DeviceData.TYPE] = 'DEVICE'
        temp[DeviceData.MACADDRESS] = c
        temp[DeviceData.RSSI] = str(random.randrange(-80, -50))
        test_str += ':'.join(temp) + '\n'

    for c in ['e', 'f']:
        temp = ['0'] * 5
        temp[BeaconData.TYPE] = 'BEACON'
        temp[BeaconData.MACADDRESS] = c
        temp[BeaconData.RSSI] = str(random.randrange(-80, -50))
        test_str += ':'.join(temp) + '\n'

    print(test_str)
    populate_graph(test_str)


    """
    args = read_args()
    print("DEBUG: Listening on port: "+str(args.port))
    plt.ion()
    plt.show()
    server_listen(args)
