import math

def a6519_sequence(n, d):
    sequence = []
    for i in range(1, n + 1):
        term = math.gcd(d ** i, i)
        sequence.append(term)
    return sequence

# Example usage:
n = 200  # Replace with the desired number of terms
sequence_n = a6519_sequence(n, 2)
print(sequence_n)

