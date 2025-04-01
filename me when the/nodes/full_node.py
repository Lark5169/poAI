from blockchain.chain import Blockchain, Block
from ai_consensus.ai_miner import AIMiner
from ai_consensus.smart_contracts.registry import ContractRegistry
import time
import hashlib
from threading import Thread, Event
import queue

class FullNode:
    def __init__(self, node_id="Node_1"):
        self.node_id = node_id
        self.blockchain = Blockchain()
        self.miner = AIMiner()
        self.contract_registry = ContractRegistry()
        self.difficulty = 4
        self.target_block_time = 30
        self.last_block_time = time.time()
        self.shutdown_event = Event()
        self.transaction_queue = queue.Queue()
        self.mining_thread = None

    def start(self):
        print(f"\n🚀 Starting {self.node_id} - Proof-of-AI Blockchain")
        print(f"🔗 Genesis hash: {self.blockchain.chain[0].hash[:16]}...")
        print(f"⚙️  Initial difficulty: {self.difficulty} zeros")
        
        self.mining_thread = Thread(target=self._mining_worker)
        self.mining_thread.start()

    def stop(self):
        print("\n⏹️ Stopping node...")
        self.shutdown_event.set()
        if self.mining_thread:
            self.mining_thread.join()
        print("Node stopped successfully")

    def _mining_worker(self):
        """Background thread that handles mining"""
        while not self.shutdown_event.is_set():
            if self.blockchain.pending_transactions:
                self._mine_pending_transactions()
            else:
                time.sleep(0.5)  # Wait if no transactions

    def _mine_pending_transactions(self):
        """Mine a block with the current pending transactions"""
        self._adjust_difficulty()
        last_block = self.blockchain.chain[-1]
        
        tx_hash = hashlib.sha256(
            str(self.blockchain.pending_transactions).encode()
        ).hexdigest()
        block_header = f"{last_block.index}{last_block.hash}{tx_hash}".encode()
        
        start_time = time.time()
        timeout = self.target_block_time * 2
        
        while (time.time() - start_time < timeout and 
               not self.shutdown_event.is_set()):
            
            ai_proof = self.miner.find_hash(block_header, self.difficulty)
            
            if ai_proof and not self.shutdown_event.is_set():
                new_block = self._create_block(last_block, ai_proof)
                if self.blockchain.add_block(new_block):
                    self._print_block_stats(new_block, ai_proof)
                    self.last_block_time = time.time()
                    return
            
            time.sleep(0.01)

    def add_transaction(self, tx):
        """Add a transaction to the processing queue"""
        if not self._validate_transaction(tx):
            return {"status": "error", "message": "Invalid transaction format"}
        
        self.transaction_queue.put(tx)
        return {"status": "queued", "message": "Transaction added to queue"}

    def process_transactions(self):
        """Process all queued transactions at once"""
        processed = []
        while not self.transaction_queue.empty():
            tx = self.transaction_queue.get_nowait()
            result = self._handle_single_transaction(tx)
            processed.append({
                "transaction": tx,
                "result": result
            })
        return {
            "status": "success",
            "processed": len(processed),
            "details": processed
        }

    def _handle_single_transaction(self, tx):
        """Process a single transaction"""
        try:
            if tx.get("tx_type") == "contract_deploy":
                return self._handle_contract_deploy(tx)
            elif tx.get("tx_type") == "contract_call":
                return self._handle_contract_call(tx)
            else:
                return self._handle_regular_transaction(tx)
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _handle_contract_deploy(self, tx):
        if not all(field in tx for field in ["contract_type", "sender"]):
            return {"status": "error", "message": "Missing required fields"}
            
        result = self.contract_registry.deploy(
            contract_type=tx["contract_type"],
            constructor_args=tx.get("args", {})
        )
        return {"status": "success", "result": result}

    def _handle_contract_call(self, tx):
        if not all(field in tx for field in ["contract_address", "function_name", "sender"]):
            return {"status": "error", "message": "Missing required fields"}
            
        contract = self.contract_registry.get_contract(tx["contract_address"])
        if not contract:
            return {"status": "error", "message": "Contract not found"}
        
        # Get the function and call it with unpacked args
        func = getattr(contract, tx["function_name"])
        return func(*tx.get("args", []), **tx.get("kwargs", {}))
    def _handle_regular_transaction(self, tx):
        """Process regular transactions"""
        self.blockchain.add_transaction(tx)
        return {"status": "success", "message": "Transaction added to pending pool"}

    def _create_block(self, last_block, ai_proof):
        """Create a new block"""
        return Block(
            index=last_block.index + 1,
            transactions=self.blockchain.pending_transactions.copy(),
            previous_hash=last_block.hash,
            ai_proof=ai_proof,
            difficulty=self.difficulty,
            timestamp=time.time()
        )

    def _adjust_difficulty(self):
        """Auto-adjust difficulty"""
        if len(self.blockchain.chain) % 5 == 0:
            avg_block_time = (time.time() - self.last_block_time) / 5
            if avg_block_time < self.target_block_time / 2:
                self.difficulty = min(8, self.difficulty + 1)
                print(f"\n🔼 Increased difficulty to {self.difficulty} zeros")
            elif avg_block_time > self.target_block_time * 1.5:
                self.difficulty = max(1, self.difficulty - 1)
                print(f"\n🔽 Decreased difficulty to {self.difficulty} zeros")

    def _print_block_stats(self, block, proof):
        """Print block mining statistics"""
        print("\n" + "═" * 60)
        print(f"💎 Block #{block.index} Mined!")
        print(f"📌 Hash: {block.hash[:16]}...{block.hash[-16:]}")
        print(f"⏱️  Mining Time: {proof['elapsed']:.2f} seconds")
        print(f"⚡ Hash Rate: {proof['hash_rate']/1e6:.2f} MH/s")
        print(f"🔢 Total Hashes: {proof['hashes']:,}")
        print(f"📊 Transactions: {len(block.transactions)}")
        print(f"🎯 Difficulty: {self.difficulty} zeros")
        print("═" * 60)

    def _validate_transaction(self, tx):
        """Validate transaction structure"""
        return isinstance(tx, dict) and "tx_type" in tx