from bob_engine import BobEngine
import sys

if __name__ == "__main__":
    engine = BobEngine()
    # Always run in background mode for this script
    engine.start_patrol(continuous=True)
