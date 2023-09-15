import math

def a6519_sequence(n):
    sequence = []
    for i in range(1, n + 1):
        term = math.gcd(2 ** i, i)
        sequence.append(term)
    return sequence

# Example usage:
n = 200  # Replace with the desired number of terms
sequence_n = a6519_sequence(n)
print(sequence_n)