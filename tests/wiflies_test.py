import unittest
import random
from ServerCode.ServerSkeleton import DeviceData, BeaconData, populate_graph, build_graph


class WifliesTest(unittest.TestCase):
    def setUp(self):

        current_fly = 'C0FFEEBEA575'

        self.test_str = current_fly + '\n'

        self.mac_to_filter = 'c'

        for c in ['a', 'b', 'c', 'd']:
            temp = ['0'] * 6
            temp[DeviceData.TYPE] = 'DEVICE'
            temp[DeviceData.MACADDRESS] = c
            temp[DeviceData.RSSI] = str(random.randrange(-80, -50))
            self.test_str += ':'.join(temp) + '\n'

        for c in ['e', 'f']:
            temp = ['0'] * 5
            temp[BeaconData.TYPE] = 'BEACON'
            temp[BeaconData.MACADDRESS] = c
            temp[BeaconData.RSSI] = str(random.randrange(-80, -50))
            self.test_str += ':'.join(temp) + '\n'

    def test_map_creation(self):
        populate_graph(self.test_str)

    def test_map_with_filter(self):
        populate_graph(self.test_str, self.mac_to_filter)