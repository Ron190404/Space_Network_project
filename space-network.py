from space_network_lib import Packet, SpaceNetwork, SpaceEntity



class BrokenConnectionError(Exception):
    pass


def attempt_transmission(network, packet):
    try:
        network.send(packet)
    except Exception:
        raise BrokenConnectionError()



class RelayPacket(Packet):
    def __init__(self, packet_to_relay, sender, proxy):

        super().__init__(packet_to_relay, sender, proxy)
        self.packet_to_relay = packet_to_relay

    def _repr_(self):
        return (f"RelayPacket (Relaying {self.packet_to_relay.content} "
                f"to {self.packet_to_relay.receiver}) from {self.sender}")



class RelaySatellite(SpaceEntity):
    def receive_signal(self, packet):
        if isinstance(packet, RelayPacket):

            print(f"Unwrapping and forwarding to {packet.packet_to_relay.receiver}")
            inner_packet = packet.packet_to_relay
            attempt_transmission(self.network, inner_packet)
        else:

            print(f"Final destination reached: {packet.content}")



if __name__ == "__main__":

    network = SpaceNetwork(level=0)


    earth = RelaySatellite("Earth", 0)
    sat1 = RelaySatellite("Sat1", 100)
    sat2 = RelaySatellite("Sat2", 200)

    earth.network = network
    sat1.network = network
    sat2.network = network


    p_final = Packet("Hello from Earth!", earth, sat2)


    p_relay = RelayPacket(p_final, earth, sat1)

    print("--- start of relayed transmission ---")
    try:
        attempt_transmission(network, p_relay)
    except BrokenConnectionError:
        print("The relay chain has failed (Fault or Distance)")