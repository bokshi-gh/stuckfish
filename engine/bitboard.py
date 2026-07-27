"""
Bitboard utilities for efficient board representation
Author: Rajesh Thapa (bokshi)
"""

def bit_scan_forward(bb):
    """Find index of least significant set bit"""
    return (bb & -bb).bit_length() - 1

def pop_lsb(bb):
    """Pop least significant bit and return index"""
    lsb = bb & -bb
    idx = lsb.bit_length() - 1
    return bb ^ lsb, idx

def count_bits(bb):
    """Count number of set bits"""
    return bb.bit_count()

def is_power_of_two(bb):
    """Check if bitboard has exactly one bit set"""
    return bb and (bb & (bb - 1)) == 0

def rank_of(sq):
    return sq >> 3

def file_of(sq):
    return sq & 7

def square_to_bit(sq):
    return 1 << sq

def bit_to_square(bit):
    return bit.bit_length() - 1

def mirror_square(sq):
    """Mirror square vertically (for black/white symmetry)"""
    return sq ^ 56

def between_squares(sq1, sq2):
    """Get bitboard of squares between sq1 and sq2"""
    if sq1 == sq2:
        return 0
    
    r1, f1 = rank_of(sq1), file_of(sq1)
    r2, f2 = rank_of(sq2), file_of(sq2)
    
    dr = r2 - r1
    df = f2 - f1
    
    if dr == 0 or df == 0 or abs(dr) == abs(df):
        step_r = 0 if dr == 0 else (1 if dr > 0 else -1)
        step_f = 0 if df == 0 else (1 if df > 0 else -1)
        
        sq = sq1 + step_r * 8 + step_f
        bb = 0
        while sq != sq2:
            bb |= 1 << sq
            sq += step_r * 8 + step_f
        return bb
    
    return 0

def ray_attacks(sq, directions, occupied):
    """Generate ray attacks from a square in given directions"""
    attacks = 0
    for dr, df in directions:
        r, f = rank_of(sq), file_of(sq)
        r += dr
        f += df
        while 0 <= r < 8 and 0 <= f < 8:
            attacks |= 1 << (r * 8 + f)
            if occupied & (1 << (r * 8 + f)):
                break
            r += dr
            f += df
    return attacks
