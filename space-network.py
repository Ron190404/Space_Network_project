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

def smart_send_packet(network, current, path):


        current_packet = Packet(current, path[-2], path[-1])

        for i in range(len(path) - 3, -1, -1):

            current_packet = RelayPacket(current_packet, path[i], path[i + 1])


        attempt_transmission(network, current_packet)


if __name__ == "__main__":
    network = SpaceNetwork(level=0)

    # Tes entités (assure-toi qu'elles ont toutes le .network = network)
    entities = [
        RelaySatellite("Earth", 0),
        RelaySatellite("Sat1", 100),
        RelaySatellite("Sat2", 200),
        RelaySatellite("Sat3", 300),
        RelaySatellite("Sat4", 400)

    ]
    for s in entities:
        s.network = network

    print("--- Test automate road (step 6) ---")

    smart_send_packet(network, "Message Automatique!", entities)