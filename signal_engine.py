import random
from datetime import datetime, timezone

def generate_signal(mine_count: int, safe_tiles: int = 5):
    """Generate random suggested coordinates; this does NOT predict real safe tiles."""
    if not 3 <= mine_count <= 10:
        raise ValueError("Mine count must be between 3 and 10.")
    if not 1 <= safe_tiles <= 25 - mine_count:
        raise ValueError("Invalid number of suggested tiles.")
    picks = sorted(random.sample(range(1, 26), safe_tiles))
    return {
        "mine_count": mine_count,
        "tiles": picks,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "method": "random suggestion (not a prediction)"
    }
