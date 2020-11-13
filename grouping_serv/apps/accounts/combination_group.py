import itertools
import random

"""
Favor data records the favorism of different people. The dictionary has key of different names,
and value as [[favored], [unfavored]] each favored person worth 1pt, unfavored person worth -1pt.
"""


def start_group(size, favor_data, total, rule):
    try:
        temp = total
        remain_group = []
        remainder = len(total) % size
        if remainder != 0:
            for i in range(remainder):
                person = random.choice(total)
                remain_group.append(person)
                total.remove(person)
                del favor_data['person']

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
        # print(groups)
        for group in groups:
            # inner.append(groups[0])
            branch(total, group, group)

        for j in score_list:
            s = 0
            diff = max(j) - min(j)
            processed_data.append(diff)

        MIN = min(processed_data)
        c = 0
        for i in processed_data:
            if i == MIN:
                min_scores.append(i)
                minimums.append(group_list[c])
            c += 1

        r = random.choice(minimums)
        if len(remain_group) > 0:
            remain_group = tuple(remain_group)
            r.append(remain_group)
        return r, 1
    except:
        return [], 0


if __name__ == "__main__":

    g = start_group(2, favor_data, total)
    print(g)