import hashlib
import random
import time
from sklearn.linear_model import LinearRegression
from collections import deque

class AIMiner:
    def __init__(self, model_id="ai_ml_v1"):
        # Mining parameters
        self.model_id = model_id
        self.hash_count = 0
        self.start_time = 0
        self.last_hashrate = 0
        
        # AI components
        self.model = LinearRegression()
        self.training_data = deque(maxlen=1000)
        self.last_prediction = None
        self.prediction_accuracy = []
        self.search_radius = 25_000_000
        self.last_success = None

    def find_hash(self, block_header, difficulty):
        """Interface method expected by FullNode"""
        self.hash_count = 0
        self.start_time = time.time()
        target = '0' * difficulty
        header = block_header.encode() if isinstance(block_header, str) else block_header
        
        # Initial AI prediction
        predicted_nonce = self._predict_initial_nonce(difficulty)
        
        while True:
            nonce = self._get_next_nonce()
            test_hash = hashlib.sha256(header + str(nonce).encode()).hexdigest()
            self.hash_count += 1
            
            # Update AI model periodically
            if self.hash_count % 1000 == 0:
                self._update_model(header, difficulty)
            
            if test_hash.startswith(target):
                elapsed = time.time() - self.start_time
                self._record_success(nonce, True)
                return {
                    'model_id': self.model_id,
                    'nonce': nonce,
                    'hash': test_hash,
                    'hashes': self.hash_count,
                    'elapsed': elapsed,
                    'hash_rate': self.hash_count / max(0.1, elapsed),
                    'ai_prediction_used': True,
                    'search_radius': self.search_radius
                }
            
            # Widen search if stuck
            if self.hash_count > 1_000_000 and self.hash_count % 500_000 == 0:
                self.search_radius = min(2**32, self.search_radius * 2)

    def _get_next_nonce(self):
        """Generate next nonce with AI guidance"""
        if self.last_prediction and random.random() < 0.7:
            offset = random.randint(-self.search_radius, self.search_radius)
            return max(0, self.last_prediction + offset)
        return random.randint(0, 2**64 - 1)

    def _predict_initial_nonce(self, difficulty):
        """Make initial nonce prediction"""
        if self.last_success:
            spread = 10_000_000 // (difficulty ** 2)
            return self.last_success + random.randint(-spread, spread)
        return random.randint(0, 2**64 - self.search_radius)

    def _update_model(self, header, difficulty):
        """Update AI model with new data"""
        features = [
            len(header),
            difficulty,
            self.hash_count,
            time.time() - self.start_time,
            self.last_hashrate,
            self.last_success or 0
        ] + [random.random() for _ in range(3)]
        
        if len(self.training_data) > 100:
            X = [x[0] for x in self.training_data]
            y = [x[1] for x in self.training_data]
            self.model.fit(X, y)
            self.last_prediction = int(self.model.predict([features])[0])
            self.last_prediction = max(0, min(self.last_prediction, 2**64 - 1))
        
        target = self.last_success if self.last_success else random.randint(0, 2**64)
        self.training_data.append((features, target))

    def _record_success(self, nonce, predicted):
        """Record successful mining"""
        self.last_success = nonce
        self.prediction_accuracy.append(predicted)
        if len(self.prediction_accuracy) > 100:
            self.prediction_accuracy.pop(0)
        self.search_radius = max(1_000_000, self.search_radius // 2)