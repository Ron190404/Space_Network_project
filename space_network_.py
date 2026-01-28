from space_network_lib import LinkTerminatedError, OutOfRangeError,BrokenConnectionError, SpaceNetwork, Packet
from satellite import Satellite, Earth,RelayPacket, attempt_transmission


if __name__ == "__main__":
    print("programme start")

    network = SpaceNetwork(level=3)

    earth = Earth("earth",0)
    sat1 = Satellite("sat1",100)
    sat2 = Satellite("sat2",200)
    final_p = Packet("Hello from Earth!",sat1, sat2)
    p_earth_to_sat1 = RelayPacket(final_p, earth, sat1)

    try:
        attempt_transmission(p_earth_to_sat1)
        print("Transmission successful")
    except BrokenConnectionError:

        print("Transmission failed")