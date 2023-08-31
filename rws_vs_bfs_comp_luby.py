import pandas as pd
import math

def a6519_sequence(n, d):
    sequence = []
    for i in range(1, n + 1):
        term = math.gcd(d ** i, i)
        sequence.append(term)
    return sequence


def luby_sequence(n, scale):
    sequence = [1]
    counts = {1: 1}
    
    for i in range(1, n):
        last_term = sequence[-1]
        
        if counts[last_term] % 2 == 0:
            next_term = scale * last_term
        else:
            next_term = 1
        
        sequence.append(next_term)
        
        if next_term in counts:
            counts[next_term] += 1
        else:
            counts[next_term] = 1
    
    return sequence


def expected_num_rws(d, g, precision, b):
  prob_succ = g / (b**d)
  prob_fail = ((b**d) - g) / b**d
 

  expected_val = 0

  exp_count = 0
  succ_count = 0

  for walk in range(0, precision):

    if seq[walk] < d:
      exp_count += seq[walk]

    else:
      succ_count += 1
      expected_val +=(exp_count + d) *  prob_succ * prob_fail**(succ_count-1) 
      # print("debug", exp_count,d,prob_succ, prob_fail**(succ_count-1), succ_count)
      exp_count += seq[walk]
          
  return expected_val + 1


def make_rws_table(depth, num_goals, precision, b):
  data = []
  for g in range(1,num_goals+1):

    data_to_append = []
    for d in range(1,depth+1):
        expected_rws = 1
        if g <= b**d: expected_rws = expected_num_rws(d, g, precision, b)
        expected_rws = round(expected_rws, 3)
        data_to_append.append(expected_rws)
        # else: data_to_append.append(1)
    data.append(data_to_append)
      # print(f"expected  of walks: {expected_rws}, depth: {d}, num_g: {g}")


  df = pd.DataFrame(data).transpose()
  # print(df)
  df.columns = [f"Num_goals={g}" for g in range(1, num_goals+1)]
  df.index = [f"Depth={d}" for d in range(1, depth+1)]
  # df = df.astype(int)  # Specify integer data type
  return df



# result_table.to_csv("result_table.csv", index=True)


def bfs_min(d, b):
  return ((b**d) - 1)/(b - 1) + 1

# is this generalization for goals g correct?
def bfs_max(d, g, b):
  return b**(d+1) - g



def make_bfs_min_table(depth, num_goals, b):
  data = []
  for g in range(1,num_goals+1):

    data_to_append = []
    for d in range(1,depth+1):
      nodes_to_expand = 2
      if g <= b ** d: nodes_to_expand = bfs_min(d, b)
      data_to_append.append(nodes_to_expand)
    data.append(data_to_append)

  df = pd.DataFrame(data).transpose()
  df.columns = [f"Num_goals={g}" for g in range(1, num_goals+1)]
  df.index = [f"Depth={d}" for d in range(1, depth+1)]
  return df


def make_bfs_max_table(depth, num_goals, b):
  data = []
  for g in range(1,num_goals+1):

    data_to_append = []
    for d in range(1,depth+1):
        nodes_to_expand = 1
        if g <= b ** d: nodes_to_expand = bfs_max(d, g, b)
        data_to_append.append(nodes_to_expand)
    data.append(data_to_append)
      # print(f"expected number of walks: {expected_rws}, depth: {d}, num_g: {g}")

  df = pd.DataFrame(data).transpose()
  df.columns = [f"Num_goals={g}" for g in range(1, num_goals+1)]
  df.index = [f"Depth={d}" for d in range(1, depth+1)]
  return df

b = 3
d = 9
g = 18
precision = 10000

luby_seq = luby_sequence(precision,2)
A6519_seq = a6519_sequence(precision, 2)

seq = luby_seq
# seq = A6519_seq


rws_result_table = make_rws_table(depth=d, num_goals=g, precision=precision, b=b)

print(f"rws table b = {b}, measuring in terms of expansions: \n {rws_result_table}")
# if not steps: print(f"rws table b = {b}, measuring in terms of random walks: \n {rws_result_table}")

bfsmin_result_table = make_bfs_min_table(d, g, b)
print(f"bfs min table b = {b}: \n {bfsmin_result_table}")

bfsmax_result_table = make_bfs_max_table(d, g, b)
print(f"bfs max table b = {b}: \n {bfsmax_result_table}")


filename = "result_tables_test_error_3_b2.csv"
# rws_result_table.to_csv(filename, mode='a', index=True)
# bfsmin_result_table.to_csv(filename, mode='a', header=False, index=True)
# bfsmax_result_table.to_csv(filename, mode='a', header=False, index=True)