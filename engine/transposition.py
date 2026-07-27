"""
Transposition table for caching evaluated positions
Author: Rajesh Thapa (bokshi)
"""

class TranspositionTable:
    def __init__(self, size=1000000):
        self.table = {}
        self.size = size
        self.hits = 0
        self.misses = 0
    
    def store(self, key, depth, score, flag, best_move, ply=0):
        """Store position in transposition table"""
        # Adjust score for mate scores
        if score > 1000000:
            score -= ply
        elif score < -1000000:
            score += ply
        
        # Limit table size
        if len(self.table) > self.size:
            self.table.clear()
        
        # Only store if deeper or equal depth
        entry = self.table.get(key)
        if entry and entry['depth'] > depth and entry['flag'] != 'exact':
            return
        
        self.table[key] = {
            'depth': depth,
            'score': score,
            'flag': flag,  # 'exact', 'lower', 'upper'
            'best_move': best_move
        }
    
    def lookup(self, key, depth, alpha, beta, ply=0):
        """Look up position in transposition table"""
        entry = self.table.get(key)
        if not entry:
            self.misses += 1
            return None
        
        self.hits += 1
        
        # Only use if stored depth is sufficient
        if entry['depth'] < depth:
            return None
        
        score = entry['score']
        
        # Adjust mate scores
        if score > 1000000:
            score += ply
        elif score < -1000000:
            score -= ply
        
        if entry['flag'] == 'exact':
            return entry['best_move'], score
        
        elif entry['flag'] == 'lower' and score >= beta:
            return entry['best_move'], score
        
        elif entry['flag'] == 'upper' and score <= alpha:
            return entry['best_move'], score
        
        return None
    
    def clear(self):
        """Clear the transposition table"""
        self.table.clear()
        self.hits = 0
        self.misses = 0
    
    def get_stats(self):
        """Get table statistics"""
        total = self.hits + self.misses
        hit_rate = self.hits / total if total > 0 else 0
        return {
            'size': len(self.table),
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': hit_rate
        }
