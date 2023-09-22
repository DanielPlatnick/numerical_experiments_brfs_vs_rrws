import sys
import math
import pandas as pd
import matplotlib.pyplot as plt


def rrw_error_adj_formula(e, d, s):
    return (e * d) / s - d * (e - 1) + 1


def a6519_helper(n):
    return n & (-n)


def a6519_sequence(n):
    sequence = []
    for i in range(1,n+1):
        sequence.append(a6519_helper(i))
    return sequence

def luby_sequence(n):
    sequence = [1]
    counts = {1: 1}
    
    for i in range(1, n):
        last_term = sequence[-1]
        
        if counts[last_term] % 2 == 0:
            next_term = 2 * last_term
        else:
            next_term = 1
        
        sequence.append(next_term)
        
        if next_term in counts:
            counts[next_term] += 1
        else:
            counts[next_term] = 1
    
    return sequence

def expected_num_luby_rws(d, g, precision, b, scale, seq):
  if g >= b**d:
    prob_succ = 1
    prob_fail = 0
  else:  
    prob_succ = g / (b**d)
    prob_fail = ((b**d) - g) / b**d
 

  expected_val = 0

  exp_count = 0
  succ_count = 0

  for walk in range(0, precision):
    current_walk = seq[walk]
    if scale == 'none':
        current_walk = current_walk
    if scale == 'd':
        current_walk = d * current_walk
    if scale == 'd/2':
        current_walk = (d/2) * current_walk
    if scale == '2d': 
        current_walk = (2 * d) * current_walk
    if scale == 'luby*2': 
        current_walk = 2 * current_walk
    if scale == 'luby*4': 
        current_walk = 4 * current_walk
    if scale == 'luby*8': 
        current_walk = 8 * current_walk
    if scale == 'luby*16': 
        current_walk = 16 * current_walk
    

    if current_walk < d:
      exp_count += current_walk

    else:
      succ_count += 1
      expected_val +=(exp_count + d) *  prob_succ * prob_fail**(succ_count-1) 
      # print("debug", exp_count,d,prob_succ, prob_fail**(succ_count-1), succ_count)
      exp_count += current_walk
          
  return expected_val + 1


def make_rws_table(depth, num_goals, precision, b, scale):
  data = []
  for g in range(1,num_goals+1):

    data_to_append = []
    for d in range(1,depth+1):
        expected_rws = 1
        if g <= b**d: expected_rws = expected_num_luby_rws(d, g, precision, b, scale)
        expected_rws = round(expected_rws,3)
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


def make_dataframe(depth, precision, branch, scale, formula, type, seq):
    to_csv = []
    for b in range(2,3):
        for d in range(2, depth+1):
            g = 0
            bfs_min = float(((b**d) - 1)/(b - 1)) + 1

            rws_expected = float('inf')
            # print(bfs_min, rws_expected)
            while rws_expected - 0.000001 >= bfs_min:
                g += 1
                s = g / (b ** d)
                if type == 'luby' or type == 'a6519':
                    rws_expected = formula(d=d, g=g, precision=precision, b=b, scale=scale, seq=seq)
                if type =='rrw_e':
                    rws_expected = formula(e=1, d=d, s=s)
                # print(rws_expected)
                # print(f"d ={d}, g={g}, rws={rws_expected}")
                print(f'd={d}, {rws_expected}, {bfs_min}, g={g}')
                if rws_expected <= bfs_min:
                    to_csv.append([b, d, g])
                    break

    df = pd.DataFrame(to_csv)
    df.columns = ["b", "d", "cutoff"]

    return df


if __name__ == '__main__':
    b = 2
    d = 15
    g = 12
    precision = 30000
    luby = luby_sequence(precision)
    a6519 = a6519_sequence(precision)
    print('hi')

    # print(expected_num_luby_rws(d=11, g=1, precision=precision, b=b, scale='none'))

    df_plot1 = make_dataframe(depth=d, precision=precision, branch=b, scale='none', formula=expected_num_luby_rws, type='luby', seq=luby)
    # df_plot2 = make_dataframe(depth=d, precision=precision, branch=b, scale='d', formula=expected_num_luby_rws, type='luby', seq=luby)
    # df_plot3 = make_dataframe(depth=d, precision=precision, branch=b, scale='d/2', formula=expected_num_luby_rws, type='luby', seq=luby)
    # df_plot4 = make_dataframe(depth=d, precision=precision, branch=b, scale='none', formula=rrw_error_adj_formula, type='rrw_e', seq=luby)
    # df_plot5 = make_dataframe(depth=d, precision=precision, branch=b, scale='2d', formula=expected_num_luby_rws, type='luby', seq=luby)
    df_plot6 = make_dataframe(depth=d, precision=precision, branch=b, scale='luby*2', formula=expected_num_luby_rws, type='luby', seq=luby)
    df_plot9 = make_dataframe(depth=d, precision=precision, branch=b, scale='luby*4', formula=expected_num_luby_rws, type='luby', seq=luby)
    df_plot10 = make_dataframe(depth=d, precision=precision, branch=b, scale='luby*8', formula=expected_num_luby_rws, type='luby', seq=luby)
    df_plot11 = make_dataframe(depth=d, precision=precision, branch=b, scale='luby*16', formula=expected_num_luby_rws, type='luby', seq=luby)






    # print(df_plot1, df_plot2, df_plot3, df_plot4)

    fig, ax = plt.subplots(figsize=(10, 6))

    # # Plot each DataFrame on the same axis
    ax.plot(df_plot1['d'], df_plot1['cutoff'], label='luby')
    # ax.plot(df_plot2['d'], df_plot2['cutoff'], label='luby_d')
    # ax.plot(df_plot3['d'], df_plot3['cutoff'], label='luby_d/2')
    # ax.plot(df_plot4['d'], df_plot4['cutoff'], label='RRWe_1')
    # ax.plot(df_plot5['d'], df_plot5['cutoff'], label='luby_2d')
    ax.plot(df_plot6['d'], df_plot6['cutoff'], label='luby_*2')
    # ax.plot(df_plot7['d'], df_plot7['cutoff'], label='a6519')
    # ax.plot(df_plot8['d'], df_plot8['cutoff'], label='a6519_d')
    ax.plot(df_plot6['d'], df_plot9['cutoff'], label='luby_*4')
    ax.plot(df_plot6['d'], df_plot10['cutoff'], label='luby_*8')
    ax.plot(df_plot6['d'], df_plot11['cutoff'], label='luby_*16')






    # Set labels and legend
    ax.set_xlabel('Depth')
    ax.set_ylabel('Goal Cutoff')
    ax.set_title(f'b = {b}')
    ax.legend()

    # Show the plot
    plt.show()




    # print(make_rws_table(depth=d, num_goals=g, precision=precision, b=b, scale='d/2'))