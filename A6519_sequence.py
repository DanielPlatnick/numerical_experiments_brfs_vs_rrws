def a6519_helper(n):
    # Perform the bitwise AND operation between n and its two's complement (-n)
    return n & (-n)
def a6519_sequence(n):
    sequence = []
    for i in range(1,n+1):
        sequence.append(a6519_helper(i))
    return sequence

precision = 500000
print(a6519_sequence(precision))