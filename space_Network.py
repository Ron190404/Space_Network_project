import time
from space_network_lib import SpaceNetwork, Packet, TemporalInterferenceError, DataCorruptedError
from satellite import Satellite

network = SpaceNetwork(level=2)

sat1 = Satellite("Sat1", 100)
sat2 = Satellite("Sat2", 200)
p = Packet("Hello Level 2!", sat1, sat2)


def attempt_transmission(packet):
    while True:
        try:
            network.send(packet)

            break
        except TemporalInterferenceError:
            print("Interference détected... wait 2s")
            time.sleep(2)
        except DataCorruptedError:
            print("Donnée failed... new essai now")


attempt_transmission(p)