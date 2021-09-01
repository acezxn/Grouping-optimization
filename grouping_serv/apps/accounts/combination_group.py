import itertools
import random
import math
import threading
import time

"""
Favor data records the favorism of different people. The dictionary has key of different names,
and value as [[favored], [unfavored]] each favored person worth 1pt, unfavored person worth -1pt.
"""

def comb(n, r):
    return math.factorial(n) // (math.factorial(r) * math.factorial(n-r))

def grouping(size, favor_data, total, rule, reward, punish, parent):
    group_list = []
    inner = []
    scores = []
    score_list = []
    processed_data = []
    minimums = []
    min_scores = []
    opt_score = []
    prev = []

    def complement(src, aux): # find other people from "src" except groupmates in "aux"
        out = []
        for i in src:
            if i not in aux:
                out.append(i)
        return tuple(out)

    def happiness_calc(group, reward, punish): # happiness calculation algorithm
        score = 0
        for member in group:
            favored = favor_data[member][0]
            avoid = favor_data[member][1]
            for single in favored:
                if single in group:
                    score += reward
            for single in avoid:
                if single in group:
                    score -= punish
        return score

    def branch(src, group, starter, parent): # recursive algorithm to list all possible outcomes of grouping
        p = group
        inner.append(group)
        other = complement(src, group)
        groups = list(itertools.combinations(other, size))
        if len(other) == size: # if other people in the class equals the group size
            inner.append(other)
            if starter not in inner:
                inner.append(starter)
            if parent not in inner and parent is not None:
                inner.append(parent)
            if len(prev) > len(inner):
                for i in prev:
                    contained = False
                    for k in inner:
                    	for j in range(size):
                            if i[j] in k:
                                contained = True
                                break
                    if not contained:
                        inner.append(i)




            prev.clear()
            prev.extend(inner)
            for g in inner:
                score = happiness_calc(g, reward, punish)
                scores.append(score)

            score_list.append(list(scores))
            group_list.append(list(inner))
            inner.clear()
            scores.clear()
            return
        elif len(other) != 0:
            for i in range(comb(len(other) -1, size - 1)):
                # print("groups:", groups)
                group = groups[i]
                branch(other, group, starter, p)

        else:
            score = happiness_calc(src, reward, punish)
            scores.append(score)
            score_list.append(list(scores))
            group_list.append([tuple(src)])

################################################################################

    groups = list(itertools.combinations(total, size))
    print("groups", len(groups), comb(len(total) - 1, size - 1))
    now = time.time() * 1000
    for i in range(comb(len(total) - 1, size - 1)):
        # inner.append(groups[0])
        group = groups[i]
        # t = threading.Thread(target=branch, args=(total, group, group, parent,))
        branch(total, group, group, parent)

        print("grouplist", group_list)
        # t.start()
        print(group, len(group_list), (time.time() * 1000) - now)
        now = time.time() * 1000
    # t.join()
    #print("grouplist", group_list)
    #print("scorelist", score_list)
    # print("scorelist: ", score_list)
    print("grouplist", group_list)
# get the most unhappy group
    if len(group_list) > 0:
        for j in score_list:
            MIN = min(j)
            #print(MIN)
            min_scores.append(MIN)
        #print("max", max(min_scores))
        print("calculated min scores")

# select the case with the happiest unhappy group
        MAX = max(min_scores)
        for j in min_scores:
            if j == MAX:
                #print('Selected score: ', score_list[min_scores.index(j)])
                minimums.append(group_list[min_scores.index(j)])
                opt_score.append(score_list[min_scores.index(j)])
                # print("find the max min")

# further optimize the optimized case

        k = []
        for h in opt_score:
              k.append(max(h))
        random.shuffle(minimums)
        r = minimums[k.index(max(k))]
        return r, 1
    else:
        return [], 1
    try:
        pass
    except Exception as e:
        #print(e)
        return [], 0


# select remainder from each case and look for the case with the happiest unhappy group
def start_group(size, favor_data, total, rule, reward, punish):
    # rule = [('user', 'user2')]
    metacase = dict()
    temp = total.copy()
    #print(favor_data)
    tmp_f = favor_data.copy()
    #print(tmp_f)
    remain_group = []
    remainder = len(total) % size # find the number of remaining people
    possible_remainders = list(itertools.combinations(total, remainder)) # find the possible remaining group

    tmp = possible_remainders.copy()

    # remove possible remaining groups which violate the rule
    for rem in tmp:
        for r in rule:
            if r[0] in rem and r[1] in rem:
                possible_remainders.remove(rem)

    #print('possible rems: ', possible_remainders)
    if remainder != 0: # if there are remaining people
        # form optimized groups for each remaining groups
        for remain_group in possible_remainders:
            favor_data = tmp_f.copy()
            total = temp.copy()
            for i in remain_group:
                total.remove(i)
                del favor_data[i]
                #print("data before run")
                #print(total)
                #print(favor_data)
            print("grouping")
            g, stat = grouping(size, favor_data, total, rule, reward, punish, None)
            print('output: ', g)
            metacase[remain_group] = g
            #print('metacase: ',metacase)
        tmp = possible_remainders.copy()

        # delete the newly generated cases which violates the rules
        for rem in tmp:
            for G in metacase[rem]:
                for r in rule:
                    if r[0] in G and r[1] in G:
                        del metacase[rem]
                        possible_remainders.remove(rem)
                        break
        favor_data = tmp_f.copy()
        total = temp.copy()
        meta_scorelist = []

        # calculating the happiness scores for the remaining groups
        for remain_group in possible_remainders:

            score_remainder = 0

            for member in remain_group:
                favored = favor_data[member][0]
                avoid = favor_data[member][1]
                for single in favored:
                    if single in remain_group:
                        score_remainder += reward
                for single in avoid:
                    if single in remain_group:
                        score_remainder -= punish
            score_statistic = []

            # recalculate the happiness of the other groups
            for groups in metacase[remain_group]:
                score = 0
                for member in groups:
                    favored = favor_data[member][0]
                    avoid = favor_data[member][1]
                    for single in favored:
                        if single in groups:
                            score += reward
                    for single in avoid:
                        if single in groups:
                            score -= punish
                    score_statistic.append(score)
            try:
                # trying to append the minimum score
                if score_remainder < min(score_statistic):
                    meta_scorelist.append(score_remainder)
                else:
                    meta_scorelist.append(min(score_statistic))
            except:
                pass
        if len(meta_scorelist) == 0:
            return [], 1

        maximum = max(meta_scorelist) # find the greatest score from the low scores
        max_scores = []
        # select the groups
        for case in possible_remainders:
            if meta_scorelist[possible_remainders.index(case)] == maximum:
                all = metacase[case].copy()
                all.append(case)
                max_scores.append(all)
        print('Select from: ', max_scores)
        print(random.choice(max_scores))
        return random.choice(max_scores), 1

    else:
        print("grouping")
        g, stat = grouping(size, favor_data, total, rule, reward, punish, None)
        tmp = g.copy()
        for group in tmp:
            for r in rule:
                if r[0] in group and r[1] in group:
                    g.remove(group)
        return g, stat


if __name__ == "__main__":
    #favor_data = {'A': [['B'], ['C']], 'B': [['C'], ['A']], 'C': [[], []], 'D': [[], []], 'E': [[], []], 'F': [[], []], 'G': [['E'], ['F']], 'H': [['G'], ['J']], 'I': [['G'], ['F']], "J": [[], []], "K": [[], []], "L": [[], []], 'M': [[], []], 'N': [[], []], "O": [[], []]}
    #total = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']

    #favor_data = {'A': [['B'], ['C']], 'B': [['C'], ['A']], 'C': [[], []], 'D': [[], []], 'E': [[], []]}
    #total = ['A', 'B', 'C', 'D', 'E']

    favor_data = {'user3': [[], []], 'user2': [['user'], []], 'user4': [[], ['user2']], 'Steven': [['user3'], ['user4']], 'user': [['user2'], []]}
    total = ['user', 'user2', 'user3', 'user4', 'Steven']
    g, stat = start_group(3, favor_data, total, [], 1, 1)


    #g, stat = grouping(3, favor_data, total, [], 1, 1, None)
    print(g, stat)
