from .block import Block

class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.create_genesis_block()
    
    def create_genesis_block(self):
        genesis = Block(0, [], "0", {"model_id": "genesis", "nonce": 0, "hash": "0"*64})
        self.chain.append(genesis)
    
    def add_block(self, new_block):
        if self.is_valid_block(new_block):
            self.chain.append(new_block)
            self.pending_transactions = []
            return True
        return False
    
    def is_valid_block(self, new_block):
        last_block = self.chain[-1]
        return all([
            new_block.index == last_block.index + 1,
            new_block.previous_hash == last_block.hash,
            new_block.hash == new_block.compute_hash(),
            new_block.ai_proof is not None
        ])