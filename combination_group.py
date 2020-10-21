import itertools
import random
'''
Favor data records the favorism of different people. The dictionary has key of different names,
and value as [[favored], [unfavored]] each favored person worth 1pt, unfavored person worth -1pt.
'''

total = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
favor_data = {'A':[['B', 'C'], ['E']], 'B':[['C'], ['D']], 'C':[['B'], ['A']], 'D':[['B'], ['E']], 'E':[['C'], ['D']], 'F':[['A'], ['C']], 'G':[['H'],['E']], 'H':[['G'], ['F']]}
size = 4
group_list = []

inner = []
def complement(src, aux):
    out = []
    for i in src:
        if i not in aux:
            out.append(i)
    return tuple(out)


def happiness_calc(group):
    score = 0
    for member in group:
        favored = favor_data[member][0]
        avoid = favor_data[member][1]
        for single in favored:
            if single in group:
                score += 1
        for single in avoid:
            if single in group:
                score -= 1
    return score

def branch(src, group, starter):
    if group != starter:
        inner.append(group)
    other = complement(src, group)
    groups = list(itertools.combinations(other, size))
    if len(other) == size:
        inner.append(other)
        inner.append(starter)
        for g in inner:
            score = happiness_calc(g)
            scores.append(score)
        score_list.append(list(scores))
        group_list.append(list(inner))
        inner.clear()
        scores.clear()

        return
    else:
        if len(other) == 0:
            inner.append(starter)
            for g in inner:
                score = happiness_calc(g)
                scores.append(score)
            score_list.append(list(scores))
            group_list.append(list(inner))
            inner.clear()
            scores.clear()
            return
    for group in groups:
        branch(other, group, starter)



scores = []
score_list = []
processed_data = []
groups = list(itertools.combinations(total, size))
# print(groups)
for group in groups:
    # inner.append(groups[0])
    branch(total, group, group)

# print(score_list)
for i in score_list:
    s = 0
    diff = max(i) - min(i)
    processed_data.append(diff)



maximums = []
max_scores = []
max = min(processed_data)
c = 0
for i in processed_data:
    if i == max:
        max_scores.append(i)
        maximums.append(group_list[c])
    c += 1

print()
r = random.choice(maximums)
print(r)
print(max_scores[maximums.index(r)])
