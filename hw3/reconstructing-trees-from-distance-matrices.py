from math import inf


def process_input():
    n = int(input())

    node_names = []
    for i in range(n):
        node_names.append(input())

    dist_mat = []

    for i in range(n):
        l = input()
        l = l.split(' ')
        l = [int(a) for a in l]
        dist_mat.append(l)

    return node_names, dist_mat


def find_closer_leaf(dist_mat, i, j):
    for k in range(len(dist_mat)):
        if k != i and k != j:
            if dist_mat[i][k] > dist_mat[j][k]:
                d = dist_mat[i][k] - dist_mat[j][k]
                return j, i, d
            else:
                d = dist_mat[j][k] - dist_mat[i][k]
                return i, j, d


def nj(dist_mat, node_names, count):
    n = len(dist_mat)

    if n == 2:
        tree_dict[node_names[0]][node_names[1]] = dist_mat[0][1]
        tree_dict[node_names[1]][node_names[0]] = dist_mat[1][0]

        return

    dist_star = [[0 for i in range(n)] for j in range(n)]
    for i in range(n):
        for j in range(n):
            dist_star[i][j] = (n - 2) * dist_mat[i][j] - sum(dist_mat[i]) - sum(dist_mat[j])

    min_dist = inf
    for i in range(n):
        for j in range(n):
            if dist_star[i][j] < min_dist and i != j:
                min_dist = dist_star[i][j]
                min_i, min_j = i, j

    delta = (sum(dist_mat[min_i]) - sum(dist_mat[min_j])) / (n - 2)

    limb_length_min_i = (dist_mat[min_i][min_j] + delta) / 2
    limb_length_min_j = (dist_mat[min_i][min_j] - delta) / 2

    tree_dict[str(count)] = {}
    tree_dict[str(count)][node_names[min_i]] = limb_length_min_i
    tree_dict[str(count)][node_names[min_j]] = limb_length_min_j

    tree_dict[node_names[min_i]][str(count)] = limb_length_min_i

    tree_dict[node_names[min_j]][str(count)] = limb_length_min_j

    # node_names.append(str(count))

    mn = min(min_i, min_j)
    mx = max(min_i, min_j)

    dist_prime = [row[:] for row in dist_mat]
    names_prime = node_names.copy()

    dist_prime.pop(mx)
    names_prime.pop(mx)
    dist_prime.pop(mn)
    names_prime.pop(mn)

    for r in dist_prime:
        r.pop(mx)
        r.pop(mn)

    m_row = []
    for k in range(len(dist_mat)):
        if k != min_i and k != min_j:
            m_row.append((dist_mat[k][min_j] + dist_mat[k][min_i] - dist_mat[min_i][min_j]) / 2)

    for i, row in enumerate(dist_prime):
        row.append(m_row[i])

    m_row.append(0)
    dist_prime.append(m_row)

    names_prime.append(str(count))
    count += 1


    nj(dist_prime, names_prime, count)


# Start
n_names, d_mat = process_input()


tree_dict = {}
for name in n_names:
    tree_dict[name] = {}

count = 0

nj(d_mat, n_names, count)
# for key, value in tree_dict.items():
#     print(f'{key}: {value}')



def scrub(parent_name, kid1_name, kid2_name, mg_name):
    tree_dict.pop(kid1_name)
    tree_dict.pop(kid2_name)

    tree_dict[parent_name].pop(kid1_name)
    tree_dict[parent_name].pop(kid2_name)

    tree_dict[mg_name] = tree_dict[parent_name]
    tree_dict.pop(parent_name)

    for k, vv in tree_dict.items():
        if vv.get(parent_name) is not None:
            vv[mg_name] = vv.pop(parent_name)



while len(tree_dict) > 4:
    min_edge = inf
    for vertex, edges in tree_dict.items():
        for v, e in tree_dict.items():
            if vertex != v:
                if len(edges) == 1 and len(e) == 1:
                    # Check if they have the same parent
                    if list(edges.items())[0][0] == list(e.items())[0][0]:
                        if list(edges.items())[0][1] < min_edge:
                            min_edge = list(edges.items())[0][1]
                            min_vertex1 = vertex
                            min_vertex2 = v
                            min_edge1 = list(edges.items())[0][1]
                            min_edge2 = list(e.items())[0][1]
                            min_parent = list(edges.items())[0][0]


    merged_name = '(' + min_vertex1 + ',' + min_vertex2 + ')'
    print(merged_name + ' ' + min_vertex1 + ' ' + str(int(min_edge1)) + ' ' + min_vertex2 + ' ' + str(int(min_edge2)))

    scrub(min_parent, min_vertex1, min_vertex2, merged_name)


for key, val in tree_dict.items():
    if len(val) != 1:
        tree_dict.pop(key)
        break

last = [(k, list(v.items())[0][1]) for k, v in tree_dict.items()]
last.sort(key=lambda x: x[1])
print(last[0][0] + ' ' + str(int(last[0][1])) + ' ' + last[1][0] + ' ' + str(int(last[1][1])) + ' ' + last[2][0] + ' ' + str(int(last[2][1])))




