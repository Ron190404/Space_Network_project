from space_network_lib import LinkTerminatedError, OutOfRangeError, SpaceNetwork, Packet



class BrokenConnectionError(Exception,):
    pass


class RelayPacket(Packet):
    def __init__(self, packet_to_relay, sender, proxy):

        super().__init__(sender=sender, receiver=proxy, content=packet_to_relay)
        self.packet_to_relay = packet_to_relay

    def _repr_(self):

        return (f"RelayPacket (Relaying {self.packet_to_relay.content} "
                f"to {self.packet_to_relay.receiver}) from {self.sender}")


def attempt_transmission(network, packet):
    try:

        network.send(packet)
        print("message send successful !!")
    except LinkTerminatedError:

        print("Link lost")
        raise BrokenConnectionError()
    except OutOfRangeError:

        print("Target out of range")
        raise BrokenConnectionError()



if __name__ == '_main_':
    print("programme start")

    network = SpaceNetwork(level=3)


    packet = Packet(sender="Sat1", receiver="Sat2", content="Hello World!")

    try:

        attempt_transmission(network, packet)
        print("Transmission successful")
    except BrokenConnectionError:

        print("Transmission failed")