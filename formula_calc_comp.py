import pandas as pd
import matplotlib.pyplot as plt

def error_adj_formula(e, d, s):
    return (e * d + 1) / s - d * (e - 1)

# print(error_adj_formula(1, 8, ))

to_csv = []
for b in range(2, 6):
    for e in range(1, 6):
        for d in range(2, 200):
            g = 0
            bfs_min = float(((b**d) - 1)/(b - 1)) + 1

            rws_expected = float('inf')
            while rws_expected - 0.000001 >= bfs_min:
                g += 1
                s = g / (b ** d)
                rws_expected = error_adj_formula(e, d, s)
                # print(d, rws_expected, bfs_min, g)

                if rws_expected <= bfs_min:
                    to_csv.append([b, e, d, g])
                    break

df = pd.DataFrame(to_csv)
df.columns = ["b", "e", "d", "cutoff"]

# Create subplots for each 'b' value
fig, axs = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle("Graphs for Different 'b' Values")

for b_value, ax in zip(range(2, 6), axs.flatten()):
    ax.set_title(f'b = {b_value}')
    ax.set_xlabel('Depth')
    ax.set_ylabel('Goals/Cutoff')

    for e_value in range(1, 6):
        data = df[(df['b'] == b_value) & (df['e'] == e_value)]
        ax.plot(data['d'], data['cutoff'], label=f'e = {e_value}')

    ax.legend()
    ax.grid(True)

plt.tight_layout()
plt.show()
