import time
import matplotlib.pyplot as plt
from market_sim.blockchain.consensus.nakamoto import NakamotoConsensus
from market_sim.blockchain.models import Block

def visualize_mining_difficulty():
    """Plots the time taken to mine a block at varying difficulty levels."""
    difficulties = range(1, 6)
    times_taken = []

    for diff in difficulties:
        consensus = NakamotoConsensus(difficulty=diff)
        consensus.add_trade("DUMMY_TRADE")
        
        start_time = time.time()
        consensus.mine_pending_trades()
        end_time = time.time()
        
        times_taken.append(end_time - start_time)
        print(f"Difficulty {diff} took {end_time - start_time:.4f} seconds")

    plt.figure(figsize=(10, 6))
    plt.plot(difficulties, times_taken, marker='o', linestyle='-', color='b')
    plt.title('Proof of Work: Mining Time vs. Target Difficulty')
    plt.xlabel('Difficulty (Number of leading zeros)')
    plt.ylabel('Time to Mine (Seconds)')
    plt.grid(True)
    plt.yscale('log')
    plt.savefig('mining_difficulty_curve.png')
    print("Saved visualization to mining_difficulty_curve.png")

if __name__ == "__main__":
    visualize_mining_difficulty()