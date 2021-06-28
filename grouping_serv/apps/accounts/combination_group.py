import itertools
import random

"""
Favor data records the favorism of different people. The dictionary has key of different names,
and value as [[favored], [unfavored]] each favored person worth 1pt, unfavored person worth -1pt.
"""


def grouping(size, favor_data, total, rule, reward, punish):
    group_list = []

    inner = []
    scores = []
    score_list = []
    processed_data = []
    minimums = []
    min_scores = []
    opt_score = []

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

    def branch(src, group, starter): # recursive algorithm to list all possible outcomes of grouping
        if group != starter:
            inner.append(group)
        other = complement(src, group)
        groups = list(itertools.combinations(other, size))
        if len(other) == size: # if other people in the class equals the group size
            inner.append(other)
            inner.append(starter)
            for g in inner:
                score = happiness_calc(g, reward, punish)
                scores.append(score)
            score_list.append(list(scores))
            group_list.append(list(inner))
            inner.clear()
            scores.clear()

            return
        else:
            if len(other) == 0: # if there is no more people in the class
                inner.append(starter)
                for g in inner:
                    score = happiness_calc(g, reward, punish)
                    scores.append(score)
                score_list.append(list(scores))
                group_list.append(list(inner))
                inner.clear()
                scores.clear()
                return
        for group in groups:
            branch(other, group, starter)

################################################################################

    groups = list(itertools.combinations(total, size))
    #print("groups", groups)
    for group in groups:
        # inner.append(groups[0])
        branch(total, group, group)
    #print("grouplist", group_list)
    #print("scorelist", score_list)

# get the most unhappy group
    if len(group_list) > 0:
        for j in score_list:
            MIN = min(j)
            #print(MIN)
            min_scores.append(MIN)
        #print("max", max(min_scores))

# select the case with the happiest unhappy group
        for j in min_scores:
            if j == max(min_scores):
                #print('Selected score: ', score_list[min_scores.index(j)])
                minimums.append(group_list[min_scores.index(j)])
                opt_score.append(score_list[min_scores.index(j)])

# further optimize the optimized case
        
        k = []
        for h in opt_score:
              k.append(max(h)) 
        random.shuffle(minimums)
        r = minimums[k.index(max(k))]
        #print(minimums)
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
    tmp_f = favor_data.copy()
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
            g, stat = grouping(size, favor_data, total, rule, reward, punish)
            #print('output: ', g)
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
        #print(meta_scorelist)

        maximum = max(meta_scorelist) # find the greatest score from the low scores
        max_scores = []

        # select the groups
        for case in possible_remainders:
            if meta_scorelist[possible_remainders.index(case)] == maximum:
                all = metacase[case].copy()
                all.append(case)
                max_scores.append(all)
        #print('Select from: ', max_scores)
        return random.choice(max_scores), 1

    else:
        g, stat = grouping(size, favor_data, total, rule, reward, punish)
        return g, stat


if __name__ == "__main__":
    favor_data = {'A': [['B'], ['C']], 'B': [['C'], ['A']], 'C': [[], []], 'D': [[], []]}
    total = ['A', 'B', 'C', 'D']
    g, stat = start_group(3, favor_data, total, [], 1, 1)
    #print(g)
