from math import inf


def print_sim_list(similarity_list, node_names):
    names = ' ' + ' '.join(node_names)
    print(names)
    for r in similarity_list:
        print(r)


def find_max_pair(sim_list):
    max_sim = -inf
    for i in range(len(sim_list)):
        for j in range(len(sim_list)):
            if i != j:
                if max_sim < sim_list[i][j]:
                    max_sim = sim_list[i][j]
                    max_coords = [i, j]

                    #    print('min nodes')
    return max_coords, max_sim


def upgma(similarity_list, node_names):
    weight_list = [1 for i in range(len(node_names))]

    while len(similarity_list) > 1:
        max_coords, max_sim = find_max_pair(similarity_list)

        # Update scores
        for i in range(len(similarity_list)):
            if not (similarity_list[max_coords[0]][i] == -inf or similarity_list[max_coords[1]][i] == -inf):
                new_score = (similarity_list[max_coords[0]][i] * (node_names[max_coords[0]].count(',')+1) + similarity_list[max_coords[1]][i] * (node_names[max_coords[1]].count(',')+1)) / ((node_names[max_coords[1]].count(',')+1) + (node_names[max_coords[0]].count(',')+1))
                similarity_list[max_coords[0]][i] = new_score
                similarity_list[i][max_coords[0]] = new_score

        # Remove row and column the second one in min pair
        similarity_list.pop(max_coords[1])
        for row in similarity_list:
            row.pop(max_coords[1])

        # Change the name list
        nds = [node_names[max_coords[0]], node_names[max_coords[1]]]
        nds = sorted(nds)
        node1 = nds[0]
        node2 = nds[1]
        node_names[max_coords[0]] = '(' + node1 + ',' + node2 + ')'
        node_names.pop(max_coords[1])

        weight_list[max_coords[0]] += 1

        merge_set_name = '(' + node1 + ',' + node2 + ')'
        left_right_similarity = int(max_sim)
        print(str(left_right_similarity) + ' ' + merge_set_name)

        # print('----------------------------------------')
        # print_sim_list(similarity_list, node_names)
        # print('----------------------------------------')



def process_input():
    n = int(input())

    node_names = []
    for i in range(n):
        node_names.append(input())

    similarity_list = []
    for i in range(n):
        l = input()
        l = l.split(' ')
        l = [float(a) for a in l]
        similarity_list.append(l)

    for i in range(len(similarity_list)):
        similarity_list[i][i] = -inf

    return similarity_list, node_names


similarity_list, node_names = process_input()
upgma(similarity_list, node_names)



