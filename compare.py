"""
Compare the three different versions of stats.
"""

import loader
import results

def compare_stats(db):
    """
    Compare the three versions of stats: compute_stats, _tulokset tables, and old results.
    """
    stats = results.compute_stats(db)
    stats_tulokset = results.get_stats_tulokset(db)
    stats_original = results.get_stats_original(db)

if __name__ == '__main__':
    db = loader.load_db()
    compare_stats(db)