from space_network_lib import SpaceEntity, LinkTerminatedError, OutOfRangeError, BrokenConnectionError, SpaceNetwork,Packet


def attempt_transmission(packet):
    network = SpaceNetwork()
    try:
        network.send(packet)
        print("message send successful !!")
    except LinkTerminatedError:
        print("Link lost")
        raise BrokenConnectionError()
    except OutOfRangeError:
        print("Target out of range")
        raise BrokenConnectionError()

class Satellite(SpaceEntity):
    def __init__(self, name:str, distance_from_earth):
        super().__init__(name, distance_from_earth)

    def receive_signal(self, packet):
        if isinstance(packet, RelayPacket):
            inner_packet = packet.data
            print(f"Unwrapping and forwarding to {inner_packet.receiver}")
            attempt_transmission(inner_packet)
        else :
            print(f"Final destination reached: {packet.data}")


class Earth(SpaceEntity):
    def __init__(self, name:str, distance_from_earth):
        super().__init__(name, distance_from_earth)

    def receive_signal(self, packet):
        print(f"{self.name} Received: {packet}")

class RelayPacket(Packet):
    def __init__(self, packet_to_relay:Packet, sender, proxy):
        super().__init__(packet_to_relay, sender, proxy)

    def __repr__(self):
        return (f"RelayPacket (Relaying {self.packet_to_relay.data} to {self.packet_to_relay.receiver}) from {self.sender}")