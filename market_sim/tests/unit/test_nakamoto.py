import unittest
from market_sim.blockchain.consensus.nakamoto import NakamotoConsensus
from market_sim.blockchain.models import Block

class MockTrade:
    """A simplified representation of the Trade object for testing."""
    def __init__(self, symbol, price, quantity):
        self.symbol = symbol
        self.price = price
        self.quantity = quantity

class TestNakamotoConsensus(unittest.TestCase):
    def setUp(self):
        self.ledger = NakamotoConsensus(difficulty=2)

    def test_genesis_block(self):
        self.assertEqual(len(self.ledger.chain), 1)
        self.assertEqual(self.ledger.chain[0].previous_hash, "0")
        self.assertTrue(self.ledger.chain[0].hash.startswith('00'))

    def test_trade_mining(self):
        t1 = MockTrade("BTC/USD", 45000, 0.5)
        t2 = MockTrade("ETH/USD", 3000, 10)
        
        self.ledger.add_trade(t1)
        self.ledger.add_trade(t2)
        
        mined_block = self.ledger.mine_pending_trades()
        
        self.assertIsNotNone(mined_block)
        self.assertEqual(mined_block.index, 1)
        self.assertEqual(len(self.ledger.chain), 2)
        self.assertTrue(mined_block.hash.startswith('00'))
        self.assertEqual(len(mined_block.transactions), 2)
        self.assertEqual(mined_block.previous_hash, self.ledger.chain[0].hash)

    def test_tampering_detection(self):
        self.ledger.add_trade(MockTrade("AAPL", 150, 100))
        self.ledger.mine_pending_trades()
        
        original_hash = self.ledger.chain[1].hash

        self.ledger.chain[1].transactions[0].quantity = 9999
        tampered_hash = self.ledger.chain[1].compute_hash()
        
        self.assertNotEqual(original_hash, tampered_hash)

if __name__ == '__main__':
    unittest.main()