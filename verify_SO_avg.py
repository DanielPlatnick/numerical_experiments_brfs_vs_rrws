
import math

def bfs_min_geo_series(b, d):
    return float(((b**d) - 1)/(b - 1)) + 1

def bfs_min_oldmin(b, d):
    return float(b**d + 1)

def bfs_avg_geo_series(b, d, g):
    return float(((b**d) - 1)/(b - 1))  - 1 + (1/(g/b**d))


depth = 5
b = 2
g = 6
n = b**depth - g
j = n - 1

def expected_val():
    val = 0
    j = n - 1
    for k in range(j):
        val += math.comb(n, k)/math.comb(b**depth, k)

    return val
        
def expected_val2():

    return (n / (b**depth - n + 1))*(1 - (math.comb(n-1,j))/ math.comb(b**depth, j)) 
    

#trying to verify formula for E[Zj]

n = 1297
j = 1296
g = 3
total_nodes = 1300
Zj_expected_1 = 0
for k in range(j + 1):
  Zj_expected_1 += (math.comb(n, k) / math.comb(total_nodes, k))

first_term = n / (total_nodes - n + 1)
second_term = 1 - (math.comb(n - 1, j) / math.comb(total_nodes, j))
Zj_expected = first_term * second_term + 1

# print(Zj_expected_1, Zj_expected)

print(1/(13/1300))