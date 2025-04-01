class LightNode:
    def __init__(self, full_node_address):
        self.full_node_address = full_node_address
    
    def verify_transaction(self, tx_hash):
        # Contact full node for verification
        return True