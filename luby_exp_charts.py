import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from luby_charts import luby_sequence
from luby_charts import a6519_sequence
from luby_charts import expected_num_luby_rws
from luby_charts import rrw_error_adj_formula

def make_exp_dataframe(depth, precision, branch, scale, formula, type, seq, goal):
    to_csv = []
    for d in range(13, depth+1):
        g = goal
        b = branch
        rws_expected = formula(d=d, g=g, precision=precision, b=b, scale=scale, seq=seq)
        print(rws_expected, d)
        to_csv.append([b, g, round(rws_expected,3), d])

    df = pd.DataFrame(to_csv)
    df.columns = ["b", "g", "expansions", "depth"]

    return df

if __name__ == "__main__":
    b = 2
    d = 18
    g = 8
    precision = 5000000
    luby = luby_sequence(precision)
    # a6519 = a6519_sequence(precision)

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    goals = [4, 8, 16, 32]
    scales = ['none', 'luby*2', 'luby*4', 'luby*8', 'luby*16']

    # Define a common y-axis limit
    common_ylim = None

    for i, goal in enumerate(goals):
        ax = axes[i // 2, i % 2]

        for scale in scales:
            df = make_exp_dataframe(depth=d, precision=precision, branch=b, scale=scale, formula=expected_num_luby_rws, type='luby', seq=luby, goal=goal)
            ax.plot(df['depth'], df['expansions'], label=f'Scale: {scale}')

            # Update the common y-axis limit based on the data
            if common_ylim is None:
                common_ylim = ax.get_ylim()
            else:
                common_ylim = (min(common_ylim[0], ax.get_ylim()[0]), max(common_ylim[1], ax.get_ylim()[1]))

        ax.set_xlabel('Depth')
        ax.set_ylabel('Expansions')
        ax.set_title(f'Expansions vs. Depth (b={b}, g={goal})')
        ax.grid(True)
        ax.legend()
        ax.get_yaxis().set_major_formatter(ScalarFormatter(useOffset=False))

    # Set the same y-axis limit for all subplots
    for i in range(2):
        for j in range(2):
            axes[i, j].set_ylim(common_ylim)

    plt.tight_layout()
    plt.show()