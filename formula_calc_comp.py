import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np

def error_adj_formula(e, d, s):
    return (e * d) / s - d * (e - 1) + 1

def error_adj_formula_old(e, d, s):
    return (e * d + 1) / s - d * (e - 1)

def bfs_min_geo_series(b, d, g):
    return float(((b**d) - 1)/(b - 1) + 1)

def bfs_max_geo_series(b, d, g):
    return float(((b**d) - 1)/(b - 1) + (b**d - g) + 1)

def hypergeo_no_replacement(n, gd, j):    
    # Calculate the expected value of non-goal nodes (Zj)
    total_nodes = n + gd
    if n == 0:
        n = 1
        j = n - 1

    first_term = n / (total_nodes - n + 1)
    second_term = 1 - (math.comb(n - 1, j) / math.comb(total_nodes, j))
    Zj_expected = first_term * second_term + 1  
    
    return Zj_expected

def bfs_avg_stack_overflow(b, d, g):
    
    # Calculate the number of non-goal nodes
    n = (b ** d) - g
    
    total_nodes_until_goal = ((b ** d) - 1) / (b - 1)
    
    #not sure if j should be n or gd here
    j = n-1

    average_goal_depth_expansions = hypergeo_no_replacement(n, g, j)
    
    final_average = total_nodes_until_goal + average_goal_depth_expansions
    # print(total_nodes_until_goal, average_goal_depth_expansions)
    return final_average

def bfs_avg_everitt(b, d, g):
    if g == 0:
        g = 1
    return float(((b**d) - 1)/(b - 1) + 1 + (1/(g/b**d)))

# # print(error_adj_formula(1, 8, ))
def make_charts(e_val, formula, depth, branch):
    to_csv = []
    for b in range(2, branch+1):
        for e in range(1, e_val+1): 
            for d in range(2, depth+1):
                g = 0
                bfs_min = formula(b,d,g)
                

                rws_expected = float('inf')
                while rws_expected - 0.000001 >= bfs_min:
                    g += 1
                    # if not abs(rws_expected - bfs_min) > 2000: g += 1
                    # else: g += 2
                    bfs_min = formula(b,d,g)
                    # bfs_avg = bfs_avg_stack_overflow(b,d,g)
                    # print(bfs_avg - bfs_min)
                    s = g / (b ** d)
                    rws_expected = error_adj_formula(e, d, s)
                    print(f"rws_expected = {rws_expected}, bfs_min = {bfs_min}, d = {d}, g = {g}, b = {b}, e = {e}")
                    # print(f"d ={d}, g={g}, rws={rws_expected}")

                    if rws_expected <= bfs_min:
                        print('hi')
                        to_csv.append([b, e, d, g])
                        break

    df = pd.DataFrame(to_csv)
    df.columns = ["b", "e", "d", "cutoff"]



    fig, axs = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle(f"RRWe Graphs with {str(formula)[10:-15]}")

    # fig.suptitle("RRWe Graphs for Different 'b' Values")

# Find the common y-axis limits for all subplots
    y_min = df['cutoff'].min()
    y_max = df['cutoff'].max()

    for b_value, ax in zip(range(2, branch+1), axs.flatten()):
        ax.set_title(f'b = {b_value}')
        ax.set_xlabel('Depth')
        ax.set_ylabel('Goals/Cutoff')

        for e_value in range(1, e_val+1):
            data = df[(df['b'] == b_value) & (df['e'] == e_value)]
            ax.plot(data['d'], data['cutoff'], label=f'e = {e_value}')
            # Add the new line y = edb
            d_values = np.arange(4, depth+1)  # Assuming the same range of d values
            # y_values = e_value * d_values * ((b_value-.9))
            y_values = (e_value * d_values * (b_value-1)) / b_value + 1
            # y_values = ((e_value*d_values)-1)*(b_value-1)+2
            y_2_values = e_value * d_values * b_value**d_values / (((b_value**d_values - 1) / (b_value - 1)) + d_values * (e_value - 1)) 
            print("y_values = e_value * d_values * (((b_value**d_values)*(b_value-1))/((b_value**d_values)-1))", y_values, "y_2_values = e_value * d_values * (b_value-1)")

            # y_values = e_value * d_values * (b_value**d_values(b_value-1))/ (b_value**d_values - 1) + b_value
            ax.plot(d_values, y_values, linestyle='--', label=f'bound {e_value} = ed(b-1) + 1', color='red')


        ax.set_ylim(y_min, y_max)  # Set the y-axis limits
        ax.legend()
        ax.grid(True)
        

    plt.tight_layout()
    plt.show()
    # Create subplots for each 'b' value
    # fig, axs = plt.subplots(2, 2, figsize=(12, 8))
    # fig.suptitle("Graphs for Different 'b' Values")

    # for b_value, ax in zip(range(2, 6), axs.flatten()):
    #     ax.set_title(f'b = {b_value}')
    #     ax.set_xlabel('Depth')
    #     ax.set_ylabel('Goals/Cutoff')

    #     for e_value in range(1, 6):
    #         data = df[(df['b'] == b_value) & (df['e'] == e_value)]
    #         ax.plot(data['d'], data['cutoff'], label=f'e = {e_value}')

    #     ax.legend()
    #     ax.grid(True)

    # plt.tight_layout()
    # plt.show()


def make_rws_table(depth, num_goals, b, error, formula_type):
    data = []
    for g in range(1,num_goals+1):

        data_to_append = []
        for d in range(1,depth+1):
            expected_rws = 1
            s = g / (b**d)
            if g <= b**d and formula_type == 1: expected_rws = error_adj_formula(error, d, s)
            elif g<= b**d and formula_type == 2: expected_rws = error_adj_formula_old(error, d, s)
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

    

def make_bfs_min_table(depth, num_goals, b):
  data = []
  for g in range(1,num_goals+1):

    data_to_append = []
    for d in range(1,depth+1):
      nodes_to_expand = 2
      if g <= b ** d: nodes_to_expand = bfs_min_geo_series(d, b)
      data_to_append.append(math.round(nodes_to_expand,3))
    data.append(data_to_append)

  df = pd.DataFrame(data).transpose()
  df.columns = [f"Num_goals={g}" for g in range(1, num_goals+1)]
  df.index = [f"Depth={d}" for d in range(1, depth+1)]
  return df

if __name__ == "__main__":
    make_charts(e_val=3, formula=bfs_max_geo_series, depth=100, branch=5)

    b = 2
    d = 15
    g = 12
    # error = 1

    # rws_result_table = make_rws_table(depth=d, num_goals=g, b=b, error=error, formula_type=1)
    # print(f"rws results table (new formula), b={b}, e={error}: \n {rws_result_table}")

    # bfsmin_result_table = make_bfs_min_table(d, g, b)
    # print(f"bfs min table b = {b}: \n {bfsmin_result_table}")

    # rws_result_table_old = make_rws_table(depth=d, num_goals=g, b=b, error=error, formula_type=2)
    # print(f"rws results table (old formula), b={b}, e={error}: \n {rws_result_table_old}")



    # filename = "result_tables_new_vs_old_formula2.csv"
    # rws_result_table.to_csv(filename, mode='a', index=True)
    # bfsmin_result_table.to_csv(filename, mode='a', header=False, index=True)
    # rws_result_table_old.to_csv(filename, mode='a', header=False, index=True)

