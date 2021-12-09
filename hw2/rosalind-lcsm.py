with open('rosalind_lcsm.txt') as f:
    lines = f.read().splitlines()
    lines.pop(0)
    inps = []
    j = 0
    for i, line in enumerate(lines):
        if 'Ros' in line:      
            inps.append(''.join(lines[j:i]))
            j = i+1

f.close()
lines = inps

len_sorted_lines = sorted(lines, key=len)
shortest_string = len_sorted_lines[0]

substrings = []
# Produce all substrings of the shortest line
for i in range(len(shortest_string)):
    for j in range(i+1, len(shortest_string)):
        substrings.append(shortest_string[i:j])
sorted_substrings = sorted(substrings, key=len, reverse=True)

# Check the substrings from longest to shortest in every other input string
# Output the first one that is in every string

for substring in sorted_substrings:
    bingo = True
    for string in len_sorted_lines[1:]:
        if substring not in string:
            bingo = False
            
    if bingo is True:
        print(substring)
        break