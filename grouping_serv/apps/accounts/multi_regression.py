import itertools
import math
import random
import threading
import concurrent.futures

def complement(src, aux): # find other people from "src" except groupmates in "aux"
    out = []
    for i in src:
        if i not in aux:
            out.append(i)
    return list(out)

def gen_case(all, size, fav_data, reward, punish, add_rem):
    g = []
    inner = []
    scores = []
    for i in all:
        inner.append(i)
        if (all.index(i) + 1) % size == 0:
            g.append(inner)
            s = happiness_calc(inner, fav_data, reward, punish)
            scores.append(s)
            inner = []
    if len(inner) != 0:
        if not add_rem:
        # Leave the remainder as a group
            g.append(inner)
            scores.append(happiness_calc(inner, fav_data, reward, punish))
        else:
        # Join the remainders to existing groups
            for i in range(len(inner)):
                # print(g[len(g)-1-i])
                g[len(g)-1-i].append(inner[i])
                del scores[len(scores)-1-i]
                scores.append(happiness_calc(g[len(g)-1-i], fav_data, reward, punish))

    return list(g), list(scores)

def test_group(MIN, max_attempts, t, sad_group, size, rule, reward, punish, fav_data, orig_groups, orig_scorelist, add_rem):
    new_min = MIN
    attempts = 0
    sg = list(sad_group)
    other = complement(t, sg)

    if len(other) != 0:
        while new_min <= MIN and attempts <= max_attempts:
            attempts += 1
            tmp = list(sg)
            for i in range(len(tmp)):
                sg.remove(tmp[i])
                r = random.choice(other)
                sg.append(r)
                other.remove(r)
                other.append(tmp[i])

            other = complement(t, sg)
            random.shuffle(other)


            groups, scorelist = gen_case(other, size, fav_data, reward, punish, add_rem)
            groups.append(list(sg))
            # groups.append("wrjonrwo")
            scorelist.append(happiness_calc(list(sg), fav_data, reward, punish))
            new_min = min(scorelist)

            violated = False

            for g in groups:
                if violated:
                    break
                for r in rule:
                    if r[0] in g and r[1] in g:
                        violated = True
                        break

            if not violated and new_min >= MIN:
                orig_groups = list(groups)
                orig_scorelist = list(scorelist)


        if new_min > MIN:
            return groups, new_min, scorelist, violated, orig_groups, orig_scorelist
        else:
            return [], MIN, scorelist, violated, orig_groups, orig_scorelist
    else:
        violated = False

        for r in rule:
            if r[0] in sg and r[1] in sg:
                violated = True
                break
        return sg, MIN, 0, violated, orig_groups, orig_scorelist

def check_violation(rule, groups):
    violated = False
    for g in groups:
        if violated:
            break
        for r in rule:
            if r[0] in g and r[1] in g:
                violated = True
                break
    return violated

def optimize(size, total, fav_data, rule, reward, punish, add_rem): # optimization based on regression
    print("RULE: ", rule)
    if size <= 0:
        return [], False
    max_attempts = 100000
    depth = 100

    t = list(total)
    random.shuffle(t)
    orig_groups, orig_scorelist = gen_case(t, size, fav_data, reward, punish, add_rem)
    print(orig_groups)
    # orig_groups, orig_scorelist = ([['E', 'P', 'Q'], ['I', 'L', 'J'], ['B', 'M', 'O'], ['A', 'F', 'K', 'C'], ['D', 'N', 'G', 'H']], [0,0,0,0,0])


    MIN = min(orig_scorelist)
    sad_group = list(orig_groups[orig_scorelist.index(MIN)])
    print(sad_group)

    other = complement(t, sad_group)
    new_min = MIN
    attempts = 0
    print(f'Standard: {MIN}')
    y = 0
    for x in range(depth):
        y = x
        with concurrent.futures.ThreadPoolExecutor() as executor:
            f1 = executor.submit(test_group, MIN, max_attempts, t, sad_group, size, rule, reward, punish, fav_data, orig_groups, orig_scorelist, add_rem)
            f2 = executor.submit(test_group, MIN, max_attempts, t, sad_group, size, rule, reward, punish, fav_data, orig_groups, orig_scorelist, add_rem)
            # groups, new_min, scorelist = f1.result()
            res1 = f1.result()
            res2 = f2.result()

            if res1[1] > res2[1]:
                groups, new_min, scorelist, violated, og, sl = res1
            else:
                groups, new_min, scorelist, violated, og, sl = res2

            # res1 = f1.result()
            # res2 = f2.result()

            tmp = list(orig_groups)

            if not check_violation(rule, og):
                orig_groups = list(og)
                orig_scorelist = list(sl)
            #
        # groups, new_min, scorelist, violated = test_group(MIN, max_attempts, t, sad_group, size, rule, reward, punish)

        print(groups, orig_groups)
        if new_min <= MIN:

            # orig_groups = list(groups)
            # orig_scorelist = list(scorelist)

            if check_violation(rule, orig_groups) and og == tmp:
                groups = []
            # elif check_violation(rule, )
            else:
                groups = list(orig_groups)
                scorelist = list(orig_scorelist)
            break

        elif new_min > MIN:
            if not violated:
                MIN = new_min
                print(f'Standard updated: {MIN}')
                orig_groups = []
                orig_scorelist = []
                orig_groups = list(groups)
                orig_scorelist = list(scorelist)
            elif x == depth - 1:
                if not check_violation(rule, orig_groups):
                    groups = list(orig_groups)
                    scorelist = list(orig_scorelist)
                else:
                    groups = []



    return groups, True





def happiness_calc(group, fav_data, reward, punish): # happiness calculation algorithm
    score = 0
    for member in group:
        favored = fav_data[member][0]
        avoid = fav_data[member][1]
        for single in favored:
            if single in group:
                score += reward
        for single in avoid:
            if single in group:
                score -= punish
    return score


if __name__ == '__main__':
    fav_data = {'user3': [[], []], 'user2': [['user'], []], 'user4': [[], ['user2']], 'Steven': [['user3'], ['user4']], 'user': [['user2'], []]}
    total = ['user2', 'user4', 'Steven', 'user3', 'user']
    g, state = optimize(2, total, fav_data, [['user', 'user2']], 1, 4, True)
    print(g)

