import multiprocessing
class PeerManager:
    def __init__(pmg,tracker):
        pmg.tracker = tracker
        pmg.peers = []
    def add_peers(pmg):
        for peer in pmg.tracker.connected_peers:
            if pmg.handshake(peer):
                pmg.peers.append(peer)
            else:
                print(f"Can't handshake with {peer.id}")
    def handshake(pmg,peer):
        try:
            handshake_message = pmg.tracker.HANDSHAKE
            peer.sent_message(handshake_message)
            print(f"new peer {peer.ip}")
            return True
        except Exception as e:
            print(f"Handshake error with {peer.ip}")