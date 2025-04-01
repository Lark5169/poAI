import time
import json
from hashlib import sha256

class Block:
    def __init__(self, index, transactions, previous_hash, ai_proof, difficulty=1):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.ai_proof = ai_proof
        self.difficulty = difficulty
        self.hash = self.compute_hash()
    
    def compute_hash(self):
        block_data = {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': [tx.to_dict() for tx in self.transactions],
            'previous_hash': self.previous_hash,
            'ai_proof': self.ai_proof,
            'difficulty': self.difficulty
        }
        block_string = json.dumps(block_data, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()