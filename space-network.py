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
        return (f"RelayPacket (Relaying {self.packet_to_relay.data} "
                f"to {self.packet_to_relay.receiver}) from {self.sender}")



class RelaySatellite(SpaceEntity):
    def receive_signal(self, packet):
        if isinstance(packet, RelayPacket):

            print(f"Unwrapping and forwarding to {packet.packet_to_relay.receiver}")
            inner_packet = packet.packet_to_relay
            attempt_transmission(self.network, inner_packet)
        else:

            print(f"Final destination reached: {packet.data}")


if __name__ == "__main__":
    network = SpaceNetwork(level=0)



    earth = RelaySatellite("Earth", 0)
    sat1 = RelaySatellite("Sat1", 100)
    sat2 = RelaySatellite("Sat2", 200)
    sat3 = RelaySatellite("Sat3", 300)
    sat4 = RelaySatellite("Sat4", 400)

    for s in [earth, sat1, sat2, sat3, sat4]:
        s.network = network

    p_final = Packet("Hello From Earth!", earth, sat4)

    p_relay3 = RelayPacket(p_final, earth, sat3)

    p_relay2 = RelayPacket(p_relay3, earth, sat2)

    p_onion = RelayPacket(p_relay2, earth, sat1)


    print("--- starting road onion ---")
    try:
        attempt_transmission(network, p_onion)
    except BrokenConnectionError:
        print("the chain broke along the way")