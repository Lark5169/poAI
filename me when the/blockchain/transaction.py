import hashlib
import json
import time
class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = time.time()
        self.hash = self.compute_hash()
    
    def compute_hash(self):
        tx_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(tx_string.encode()).hexdigest()
    
    def to_dict(self):
        return self.__dict__