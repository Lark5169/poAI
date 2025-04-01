import socket
import threading
import json

class P2PNode:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.peers = set()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.blockchain = None
    
    def start(self, blockchain):
        self.blockchain = blockchain
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        threading.Thread(target=self.accept_connections).start()
    
    def accept_connections(self):
        while True:
            conn, addr = self.socket.accept()
            self.peers.add(addr)
            threading.Thread(target=self.handle_connection, args=(conn,)).start()
    
    def handle_connection(self, conn):
        while True:
            data = conn.recv(1024)
            if not data:
                break
            message = json.loads(data.decode())
            self.handle_message(message)
    
    def handle_message(self, message):
        if message['type'] == 'block':
            self.blockchain.add_block(message['data'])