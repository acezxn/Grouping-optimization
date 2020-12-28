import itertools
import random

"""
Favor data records the favorism of different people. The dictionary has key of different names,
and value as [[favored], [unfavored]] each favored person worth 1pt, unfavored person worth -1pt.
"""


def start_group(size, favor_data, total, rule):
    # rule = [('user', 'user2')]
    temp = total
    remain_group = []
    remainder = len(total) % size
    if remainder != 0:
        for i in range(remainder):
            person = random.choice(total)
            remain_group.append(person)
            total.remove(person)
            del favor_data[person]

    group_list = []

    inner = []
    scores = []
    score_list = []
    processed_data = []
    minimums = []
    min_scores = []
    # return [size, favor_data, total]

    #

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

    groups = list(itertools.combinations(total, size))
    print("groups", groups)
    for group in groups:
        # inner.append(groups[0])
        branch(total, group, group)
    print("grouplist", group_list)
    tmp = group_list
    case2rm = []
    for case in tmp:
        print("case",case)
        for g in case: # groups
            print("group",g)
            for r in rule:
                print(r[0], r[1])
                if r[0] in list(g) and r[1] in list(g):
                    # print(group_list)
                    try:
                        print(len(group_list), len(score_list))
                        print(score_list)
                        print(score_list[group_list.index(case)])
                        idx = group_list.index(case)
                        case2rm.append(idx)
                        # group_list.remove(case)
                        # score_list.remove(score_list[idx])
                        break
                    except:
                        pass

    for i in case2rm:
        group_list.remove(group_list[i])
        score_list.remove(score_list[i])

    print("grouplist", group_list)
    print("scorelist", score_list)
    if len(group_list) > 0:
        for j in score_list:
            s = 0
            diff = max(j) - min(j)
            processed_data.append(diff)
        print("processed data", processed_data)
        MIN = min(processed_data)
        c = 0
        for i in processed_data:
            if i == MIN:
                min_scores.append(i)
                minimums.append(group_list[c])
            c += 1
        print("minimums", minimums)
        r = random.choice(minimums)
        if len(remain_group) > 0:
            remain_group = tuple(remain_group)
            r.append(remain_group)
        return r, 1
    else:
        return [], 1
    try:
        pass
    except Exception as e:
        print(e)
        return [], 0


if __name__ == "__main__":
    favor_data = [['A', ['B'], ['C']], ['B', ['C'], ['A']]]
    total = ['A', 'B']
    g = start_group(2, favor_data, total, [])
    print(g)
