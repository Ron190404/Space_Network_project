from space_network_lib import SpaceNetwork, Packet
from satellite import Satellite


network = SpaceNetwork()

sat_1 = Satellite("sat1",100)
sat_2 = Satellite("sat2",200)

message = Packet("hello !", sat_1, sat_2)
network.send(message)