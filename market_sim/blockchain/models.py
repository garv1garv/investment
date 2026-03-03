import hashlib
import json
from time import time
from typing import List, Any

class Block:
    """Represents a single block in the State Machine Replication log."""
    
    def __init__(self, index: int, transactions: List[Any], previous_hash: str, timestamp: float = None, nonce: int = 0):
        self.index = index
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.timestamp = timestamp or time()
        self.nonce = nonce
        self.hash = self.compute_hash()

    def compute_hash(self) -> str:
        """Serializes the block and computes its SHA-256 hash."""
        tx_list = [
            tx.__dict__ if hasattr(tx, '__dict__') else str(tx) 
            for tx in self.transactions
        ]
        
        block_data = {
            "index": self.index,
            "transactions": tx_list,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "nonce": self.nonce
        }
        
        block_string = json.dumps(block_data, sort_keys=True, default=str).encode()
        return hashlib.sha256(block_string).hexdigest()