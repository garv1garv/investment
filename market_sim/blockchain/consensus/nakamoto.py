from typing import List, Optional
from market_sim.blockchain.models import Block

class NakamotoConsensus:
    """
    Implements the Proof-of-Work longest-chain consensus as described 
    in 'Foundations of Distributed Consensus and Blockchains'.
    """
    
    def __init__(self, difficulty: int = 3):
        self.difficulty = difficulty
        self.chain: List[Block] = []
        self.unconfirmed_trades: List = []
        self._create_genesis_block()

    def _create_genesis_block(self):
        """Initializes the blockchain with a hardcoded genesis block."""
        genesis_block = Block(0, [], "0")
        self.mine_block(genesis_block)
        self.chain.append(genesis_block)

    def get_last_block(self) -> Block:
        """Returns the most recent block in the longest chain."""
        return self.chain[-1]

    def add_trade(self, trade):
        """Queues a trade from the MatchingEngine to be included in the next block."""
        self.unconfirmed_trades.append(trade)

    def mine_block(self, block: Block) -> str:
        """Proof of Work: find a nonce such that the block hash meets the difficulty target."""
        block.nonce = 0
        computed_hash = block.compute_hash()
        
        target_prefix = '0' * self.difficulty
        while not computed_hash.startswith(target_prefix):
            block.nonce += 1
            computed_hash = block.compute_hash()
            
        block.hash = computed_hash
        return computed_hash

    def mine_pending_trades(self) -> Optional[Block]:
        """Bundles pending trades, solves the PoW puzzle, and appends the block."""
        if not self.unconfirmed_trades:
            return None
            
        last_block = self.get_last_block()
        new_block = Block(
            index=last_block.index + 1,
            transactions=self.unconfirmed_trades.copy(),
            previous_hash=last_block.hash
        )
        
        self.mine_block(new_block)
        self.chain.append(new_block)
        
        self.unconfirmed_trades = []
        return new_block