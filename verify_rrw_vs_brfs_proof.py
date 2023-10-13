from formula_calc_comp import error_adj_formula
from formula_calc_comp import bfs_min_geo_series
from formula_calc_comp import bfs_max_geo_series
from formula_calc_comp import bfs_avg_stack_overflow

def verify_proofs(e_val, formula, depth, branch):
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
                    # print(f"rws_expected = {rws_expected}, bfs_min = {bfs_min}, d = {d}, g = {g}, b = {b}, e = {e}")
                    # print(f"d ={d}, g={g}, rws={rws_expected}")

                    if rws_expected <= bfs_min:
                        # print('hi')
                        to_csv.append([b, e, d, g])
                        break
    return to_csv

def test_g_vs_brfsmin_cutoff(values_to_test):
    failure = False
    for values in values_to_test:
        b = values[0]
        e = values[1]
        d = values[2]
        g = values[3]

        # print(f"g = {g} compare = {e*d*(b-1) + 1}")
        if g > e*d*(b-1) + 1:
            failure = True
            print ("fail", g, e*d*(b-1)+1)
    if failure: return "failure"
    return "success"

def test_g_vs_brfsmax_cutoff(values_to_test):
    failure = False
    for values in values_to_test:
        b = values[0]
        e = values[1]
        d = values[2]
        g = values[3]

        if g > (e*d*(b-1)/b) + 1:
            failure = True
            print (f"fail, g = {g}, (e*d*(b-1)/b) + 1 = {(e*d*(b-1)/b) + 1} ")
    if failure: return "failure"
    return "success"

def test_g_vs_brfsSOavg_cutoff(values_to_test):
    failure = False
    for values in values_to_test:
        b = values[0]
        e = values[1]
        d = values[2]
        g = values[3]

        # print(f"g = {g} compare = {e*d*(b-1) + 1}")
        if g > ((e*d)-1)*(b-1)+2:
            failure = True
            print (f"fail, g={g}, values = g={g}, b={b}, d={d}, e={e}, avg = ((e*d)-1)*(b-1)+1) --> {((e*d)-1)*(b-1)+2}")
    if failure: return "failure"
    return "success"


if __name__ == "__main__":
    # min_values_to_test = verify_proofs(e_val=4, formula=bfs_min_geo_series, depth=150, branch=10)
    # min_verification = test_g_vs_brfsmin_cutoff(min_values_to_test)
    # print(min_verification)

    max_values_to_test = verify_proofs(e_val=4, formula=bfs_max_geo_series, depth=150, branch=20)
    max_verification = test_g_vs_brfsmax_cutoff(max_values_to_test)
    print(max_verification)

    # avg_values_to_test = verify_proofs(e_val=3, formula=bfs_avg_stack_overflow, depth=60, branch=4)
    # avg_verification = test_g_vs_brfsSOavg_cutoff(avg_values_to_test)
    # print(avg_verification)
