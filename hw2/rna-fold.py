def is_complement(n1, n2):
    if (n1 == 'U' and n2 == 'A') or (n1 == 'A' and n2 == 'U') or (n1 == 'C' and n2 == 'G') or (n1 == 'G' and n2 == 'C'):
        return 1
    else:
        return 0


def nussinove_algorithm(s):
    table = [[0 for i in range(len(s))] for j in range(len(s))]

    # Only loop through the upper triangular part of the matrix
    for m in range(1, len(s)):
        for n in range(m, len(s)):
            i = n - m
            j = n
            case1 = table[i+1][j]
            case2 = table[i][j-1]
            case3 = table[i+1][j-1] + is_complement(s[i], s[j])
            if abs(i-j) != 1:
                case4 = max([table[i][k] + table[k+1][j] for k in range(i+1, j)])
            else:
                case4 = -1

            table[i][j] = max(case1, case2, case3, case4)

    return table


def trace_back(s, table):
    stack = []
    pairs = []
    i, j = (0, len(s)-1)
    stack.append((i, j))

    while len(stack) != 0:
        i, j = stack.pop()
        if i >= j:
            continue
        elif table[i+1][j] == table[i][j]:
            stack.append((i+1, j))
        elif table[i][j-1] == table[i][j]:
            stack.append((i, j-1))
        elif table[i+1][j-1] + is_complement(s[i], s[j]) == table[i][j]:
            pairs.append((i, j))
            stack.append((i+1, j-1))
        else:
            # right inclusive or exclusive?
            for k in range(i+1, j):
                if table[i][k] + table[k+1][j] == table[i][j]:
                    stack.append((k+1, j))
                    stack.append((i, k))
                    break

    return pairs


s = input()

tab = nussinove_algorithm(s)
ps = trace_back(s, tab)
print(tab[0][-1])
for i, j in ps:
    print(str(i+1) + ' ' + str(j+1))


