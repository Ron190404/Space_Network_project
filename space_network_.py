from space_network_lib import LinkTerminatedError, OutOfRangeError, SpaceNetwork, Packet


# Étape 3.2 : Création de l'exception personnalisée
class BrokenConnectionError(Exception,):
    pass
    """Exception levée pour les erreurs de connexion non récupérables."""
    pass


# Étape 3.2 : Mise à jour de la fonction de transmission
def attempt_transmission(network, packet):
    try:
        # On tente l'envoi via la bibliothèque
        network.send(packet)
        print("message send successful !!")
    except LinkTerminatedError:
        # Affichage du message spécifique et levée de l'exception personnalisée
        print("Link lost")
        raise BrokenConnectionError()
    except OutOfRangeError:
        # Affichage du message spécifique et levée de l'exception personnalisée
        print("Target out of range")
        raise BrokenConnectionError()


# Étape 3.1 & 3.3 : Bloc principal (Main)
if __name__ == '_main_':
    print("programme start")
    # Initialisation avec level=3
    network = SpaceNetwork(level=3)

    # Création d'un objet Packet (indispensable pour éviter l'AttributeError)
    packet = Packet(sender="Sat1", receiver="Sat2", content="Hello World!")

    try:
        # Tentative d'envoi protégé par un try/except
        attempt_transmission(network, packet)
        print("Transmission successful")
    except BrokenConnectionError:
        # Étape 3.3 : Message d'erreur final si la connexion est rompue
        print("Transmission failed")