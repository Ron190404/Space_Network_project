from space_network_lib import SpaceEntity

class Satellite(SpaceEntity):
    def __init__(self, name, distance_from_earth):
        super().__init__(name, distance_from_earth)
        self.distance_from_earth = distance_from_earth

    def receive_signal(self, packet):
        print(f"{self.name} Received: {packet}")