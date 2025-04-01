from flask import Flask, jsonify, request
from blockchain.transaction import Transaction
app = Flask(__name__)
blockchain = None

def start_api(blockchain_instance, port=5000):
    global blockchain
    blockchain = blockchain_instance
    app.run(port=port)

@app.route('/blocks', methods=['GET'])
def get_blocks():
    return jsonify([block.__dict__ for block in blockchain.chain])

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400
    
    tx = Transaction(values['sender'], values['recipient'], values['amount'])
    blockchain.pending_transactions.append(tx)
    return "Transaction added", 201