from math import inf


def similarity_score(char1, char2):
    if char1 == char2:
        return 1
    else:
        return -2


def trace_back(q1, q2, q3, trace_t):
    str1 = ''
    str2 = ''
    str3 = ''

    i, j, k = (len(q1), len(q2), len(q3))

    while (i, j, k) != (0, 0, 0):
        prev_i, prev_j, prev_k = trace_t[i][j][k]

        if (prev_i, prev_j, prev_k) == (-1, 0, 0):
            str1 = q1[i-1] + str1
            str2 = '-' + str2
            str3 = '-' + str3

        elif (prev_i, prev_j, prev_k) == (0, -1, 0):
            str1 = '-' + str1
            str2 = q2[j-1] + str2
            str3 = '-' + str3

        elif (prev_i, prev_j, prev_k) == (0, 0, -1):
            str1 = '-' + str1
            str2 = '-' + str2
            str3 = q3[k-1] + str3

        elif (prev_i, prev_j, prev_k) == (-1, -1, 0):
            str1 = q1[i-1] + str1
            str2 = q2[j-1] + str2
            str3 = '-' + str3

        elif (prev_i, prev_j, prev_k) == (-1, 0, -1):
            str1 = q1[i-1] + str1
            str2 = '-' + str2
            str3 = q3[k-1] + str3

        elif (prev_i, prev_j, prev_k) == (0, -1, -1):
            str1 = '-' + str1
            str2 = q2[j-1] + str2
            str3 = q3[k-1] + str3

        elif (prev_i, prev_j, prev_k) == (-1, -1, -1):
            str1 = q1[i-1] + str1
            str2 = q2[j-1] + str2
            str3 = q3[k-1] + str3

        i, j, k = i + prev_i, j + prev_j, k + prev_k
    return str1, str2, str3


def score_alignments(str1, str2, str3):
    match_score = 1
    mismatch_score = -2
    gap_penalty = -3

    gap_count = 0
    mismatch_count = 0
    match_count = 0

    aligned_strs = [str1, str2, str3]

    for i in range(len(str1)):
        for strand in aligned_strs:
            if strand[i] == '-':
                gap_count += 1

        char1 = str1[i]
        char2 = str2[i]
        char3 = str3[i]

        if not (char1 == '-' or char2 == '-'):
            if char1 == char2:
                match_count += 1
            else:
                mismatch_count += 1

        if not (char1 == '-' or char3 == '-'):
            if char1 == char3:
                match_count += 1
            else:
                mismatch_count += 1

        if not (char2 == '-' or char3 == '-'):
            if char2 == char3:
                match_count += 1
            else:
                mismatch_count += 1

    overall_score = match_count * match_score + mismatch_count * mismatch_score + gap_count * gap_penalty
    return overall_score


def needleman_wunsch_3d(query1, query2, query3):
    gap_penalty = -3
    max_score = -inf

    score_table = [[[-inf for i in range(len(query3) + 1)] for j in range(len(query2) + 1)] for k in
                   range(len(query1) + 1)]
    score_table[0][0][0] = 0

    trace_table = [[[(0, 0, 0) for i in range(len(query3) + 1)] for j in range(len(query2) + 1)] for k in
                   range(len(query1) + 1)]
    trace_dict = {1: (-1, 0, 0), 2: (0, -1, 0), 3: (0, 0, -1), 4: (-1, -1, 0),
                  5: (-1, 0, -1), 6: (0, -1, -1), 7: (-1, -1, -1)}
    filled = (0, 0, 0)

    for i in range(len(query1) + 1):
        for j in range(len(query2) + 1):
            for k in range(len(query3) + 1):
                if (i, j, k) == filled:
                    continue

                cases = [-inf, -inf, -inf, -inf, -inf, -inf, -inf]

                if i - 1 >= 0:
                    cases[0] = score_table[i - 1][j][k] + 2 * gap_penalty
                if j - 1 >= 0:
                    cases[1] = score_table[i][j - 1][k] + 2 * gap_penalty
                if k - 1 >= 0:
                    cases[2] = score_table[i][j][k - 1] + 2 * gap_penalty
                if i - 1 >= 0 and j - 1 >= 0:
                    cases[3] = score_table[i - 1][j - 1][k] + gap_penalty + similarity_score(query1[i-1], query2[j-1])
                if i - 1 >= 0 and k - 1 >= 0:
                    cases[4] = score_table[i - 1][j][k - 1] + gap_penalty + similarity_score(query1[i-1], query3[k-1])
                if j - 1 >= 0 and k - 1 >= 0:
                    cases[5] = score_table[i][j - 1][k - 1] + gap_penalty + similarity_score(query2[j-1], query3[k-1])
                if i - 1 >= 0 and j - 1 >= 0 and k - 1 >= 0:
                    cases[6] = score_table[i - 1][j - 1][k - 1] + (similarity_score(query1[i-1], query2[j-1]) +
                                                                   similarity_score(query1[i-1], query3[k-1]) +
                                                                   similarity_score(query2[j-1], query3[k-1]))

                best_score = max(cases)
                best_score_indices = cases.index(best_score)
                trace_indices = trace_dict[best_score_indices+1]

                score_table[i][j][k] = best_score
                trace_table[i][j][k] = trace_indices

                if best_score > max_score:
                    max_score = best_score

    return trace_table

s1, s2, s3 = input(), input(), input()
tr_table = needleman_wunsch_3d(s1, s2, s3)
a1, a2, a3 = trace_back(s1, s2, s3, tr_table)
score = score_alignments(a1, a2, a3)
print(score)

