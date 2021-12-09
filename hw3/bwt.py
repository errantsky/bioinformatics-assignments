
# coding: utf-8

# ## Bio Homework 3
# 
# ### Sepehr Torabparhiz
# ### 93100774

# ### Q1: BWT

# coding: utf-8

# ## Bio Homework 3
# 
# ### Sepehr Torabparhiz
# ### 93100774

# ### Q1: BWT


# coding: utf-8

# ## Bio Homework 3
# 
# ### Sepehr Torabparhiz
# ### 93100774

# ### Q1: BWT

# coding: utf-8

# ## Bio Homework 3
# 
# ### Sepehr Torabparhiz
# ### 93100774

# ### Q1: BWT


from functools import cmp_to_key


val_dict = {'$': 0, 'A': 1, 'C': 2, 'G': 3, 'T': 4}


class Suffix:
    def __init__(self, index, rank):
        self.index = index
        self.rank = rank


def compare(suffix1, suffix2):
    if suffix1.rank[0] == suffix2.rank[0]:
        if suffix1.rank[1] < suffix2.rank[1]:
            return -1
        else:
            return 1
    else:
        if suffix1.rank[0] < suffix2.rank[0]:
            return -1
        else:
            return 1


def print_suffix(s, index):
    print(s[index:])


def radix_sort(a):
    n = len(a)
    max_len = 0
    for num in a:
        if len(str(num)) > max_len:
            max_len = len(str(num))

    for x in range(max_len):
        bins = [[] for i in range(n)]
        for y in a:
            bins[(y // n ** x) % n].append(y)
        a = []
        for section in bins:
            a.extend(section)
    return a


def make_bwt(s, suffix_array):
    bwt = ['a' for i in range(len(s))]
    for i in range(len(s)):
        if suffix_array[i] > 0:
            bwt[i] = s[suffix_array[i] - 1]
        else:
            bwt[i] = '$'
    return ''.join(bwt)


def make_first_column(s, suffix_array):
    first_column = ['a' for i in range(len(s))]
    for i, ind in enumerate(suffix_array):
        first_column[i] = s[ind]

    return ''.join(first_column)


def make_suffix_array(s):
    suffix_list = []

    for i in range(len(s)):
        suffix = Suffix(index=i,
                        rank=[val_dict[s[i]],
                              (-1 if i + 1 >= len(s)
                               else val_dict[s[i + 1]])])

        suffix_list.append(suffix)

    suffix_list = sorted(suffix_list, key=cmp_to_key(compare))
    index_list = [0 for i in range(len(s))]

    k = 4
    while k < 2 * len(s):
        rank = 0
        prev_rank = suffix_list[0].rank[0]
        suffix_list[0].rank[0] = rank
        index_list[suffix_list[0].index] = 0

        for i in range(1, len(s)):
            if (suffix_list[i].rank[0] == prev_rank and
                        suffix_list[i].rank[1] == suffix_list[i - 1].rank[1]):
                prev_rank = suffix_list[i].rank[0]
                suffix_list[i].rank[0] = rank
            else:
                prev_rank = suffix_list[i].rank[0]
                rank += 1
                suffix_list[i].rank[0] = rank

            index_list[suffix_list[i].index] = i

        for i in range(len(s)):
            next_index = suffix_list[i].index + k // 2
            suffix_list[i].rank[1] = (-1 if next_index >= len(s)
                                      else suffix_list[index_list[next_index]].rank[0])

        suffix_list = sorted(suffix_list, key=cmp_to_key(compare))

        k = k * 2

    suffix_array = [suffix_list[i].index for i in range(len(s))]

    return suffix_array


def check_reads(s, bwt, suffix_array, reads):
    for read in reads:
        found_flag1 = False
        found_flag2 = False
        # First pass
        for i, ind in enumerate(suffix_array):
            if s[ind:ind + len(read)] == read:
                first = str(i + 1)
                found_flag1 = True
                break

        if found_flag1 is False:
            print('not found')
            continue

        # Second pass
        for i, ind in enumerate(suffix_array[::-1]):
            if s[ind:ind + len(read)] == read:
                last = str(len(s) - i)
                break

        print(first + ' ' + last)


s = input()
s = s + '$'
t = int(input())
suff_arr = make_suffix_array(s)
bwt = make_bwt(s, suff_arr)

reads = []
for i in range(t):
    reads.append(input())
print(bwt)
check_reads(s, bwt, suff_arr, reads)


