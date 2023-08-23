def luby_sequence(i):
    if i == 0:
        return 1

    k = 1
    while (2**k - 1) < i:
        k += 1

    #case 1
    if i == 2**k - 1:
        return 2**(k - 1)

    #case 2
    elif 2**(k-1) <= i < 2**k - 1:
        return luby_sequence(i - 2**(k - 1)+1)

for i in range(1, 200):
    print(luby_sequence(i), end=" ")