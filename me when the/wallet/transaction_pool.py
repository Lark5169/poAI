class TransactionPool:
    def __init__(self):
        self.transactions = []
    
    def add_transaction(self, transaction):
        self.transactions.append(transaction)
    
    def clear(self):
        self.transactions = []