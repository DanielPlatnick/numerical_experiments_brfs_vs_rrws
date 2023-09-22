import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np

def error_adj_formula(e, d, s):
    return (e * d) / s - d * (e - 1) + 1

def error_adj_formula_old(e, d, s):
    return (e * d + 1) / s - d * (e - 1)


# # print(error_adj_formula(1, 8, ))
def make_charts(e_val):
    to_csv = []
    for b in range(2, 6):
        for e in range(1, e_val): 
            for d in range(2, 11):
                g = 0
                bfs_min = float(((b**d) - 1)/(b - 1)) + 1

                rws_expected = float('inf')
                while rws_expected - 0.000001 >= bfs_min:
                    g += 1
                    s = g / (b ** d)
                    rws_expected = error_adj_formula(e, d, s)
                    # print(f"d ={d}, g={g}, rws={rws_expected}")

                    if rws_expected <= bfs_min:
                        to_csv.append([b, e, d, g])
                        break

    df = pd.DataFrame(to_csv)
    df.columns = ["b", "e", "d", "cutoff"]



    fig, axs = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle("RRWe Graphs for Different 'b' Values")

# Find the common y-axis limits for all subplots
    y_min = df['cutoff'].min()
    y_max = df['cutoff'].max()

    for b_value, ax in zip(range(2, 6), axs.flatten()):
        ax.set_title(f'b = {b_value}')
        ax.set_xlabel('Depth')
        ax.set_ylabel('Goals/Cutoff')

        for e_value in range(1, e_val):
            data = df[(df['b'] == b_value) & (df['e'] == e_value)]
            ax.plot(data['d'], data['cutoff'], label=f'e = {e_value}')
            # Add the new line y = edb
            d_values = np.arange(2, 11)  # Assuming the same range of d values
            y_values = e_value * d_values * (b_value-1) + (2)  # Calculate y = edb
            ax.plot(d_values, y_values, linestyle='--', label=f'bound {e_value} = ed(b-.5)', color='red')

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

def bfs_min(d, g, b):
    return ((b**d) - 1)/(b - 1) + 1

def make_bfs_min_table(depth, num_goals, b):
  data = []
  for g in range(1,num_goals+1):

    data_to_append = []
    for d in range(1,depth+1):
      nodes_to_expand = 2
      if g <= b ** d: nodes_to_expand = bfs_min(d, g, b)
      data_to_append.append(math.round(nodes_to_expand,3))
    data.append(data_to_append)

  df = pd.DataFrame(data).transpose()
  df.columns = [f"Num_goals={g}" for g in range(1, num_goals+1)]
  df.index = [f"Depth={d}" for d in range(1, depth+1)]
  return df

if __name__ == "__main__":
    make_charts(4)

    b = 3
    d = 15
    g = 12
    error = 1

    rws_result_table = make_rws_table(depth=d, num_goals=g, b=b, error=error, formula_type=1)
    print(f"rws results table (new formula), b={b}, e={error}: \n {rws_result_table}")

    bfsmin_result_table = make_bfs_min_table(d, g, b)
    print(f"bfs min table b = {b}: \n {bfsmin_result_table}")

    rws_result_table_old = make_rws_table(depth=d, num_goals=g, b=b, error=error, formula_type=2)
    print(f"rws results table (old formula), b={b}, e={error}: \n {rws_result_table_old}")



    filename = "result_tables_new_vs_old_formula2.csv"
    # rws_result_table.to_csv(filename, mode='a', index=True)
    # bfsmin_result_table.to_csv(filename, mode='a', header=False, index=True)
    # rws_result_table_old.to_csv(filename, mode='a', header=False, index=True)

