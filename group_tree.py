import random
total = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
wills = [['A', ['B', 'C', 'D']], ['B', ['C', 'D', 'A']], ['C', ['D']], [
    'D', ['A', 'B']], ['E', ['F']], ['F', ['E']], ['G', ['F']], ['H', []]]
group_size = 4

generated = []
def gen(n):
    i = random.choice(n)
    while i in generated:
        i = random.choice(n)
    generated.append(i)
    return i

rating_list = []
grouped = []
groups = []
selection = ""

def randomly_choose():
    print("No ideal points left, randomly assigning")
    c = random.randint(0, len(total)-1)
    while total[c] in grouped:
        c = random.randint(0, len(total)-1)
    selection = total[c]
    return selection


for x in range(len(total)):
    print(len(total), len(grouped))
    if len(total) - len(grouped) == group_size:
        remain = []
        for y in total:
            if y not in grouped:
                remain.append(y)
        print(remain)
        groups.append(remain)
        break
    i = gen(range(len(total)))
    repeated = False
    target = wills[i][0]
    for k in grouped:
        if k == target:
            repeated = True
            break
    if repeated:
        continue
    tar_idx = i
    wanter = wills[i][1]
    rating_list = []
    group = [target]
    grouped.append(target)
    for iter in range(group_size-1):
        for j in range(len(wanter)):
            want_idx_in_total = total.index(wanter[j])
            wanted_num = len(wills[want_idx_in_total][1])
            rating_list.append(wanted_num)
        try:
            value = min(rating_list)
            index = rating_list.index(value)
            c = index
            selection = wanter[index]
            print(target, wanter, index, grouped)
            for L in grouped:
                index = rating_list.index(value)
                # print(L, selection)
                if L == selection:
                    repeated = True
                    print("Ideal point taken, Finding other points")
                    for idx in range(len(wanter)):
                        print("wanter[idx]", wanter[idx], "G: ", grouped)
                        if wanter[idx] not in grouped:
                            c = idx
                            selection = wanter[c]
                            # print("selection: ", selection)
                            repeated = False
                            break
                    if repeated:
                        print("All point taken, jumping")
                        for member in group:
                            src = member
                            print(f'Jumping from "{src}')
                            collection = []
                            lengths = []
                            for m in wills:
                                print('m', m[0], m[1], src in m[1], m[0] not in grouped, m[0] != src, not (m[0] in wanter))
                                print(m[0], wanter)
                                if src in m[1] and m[0] not in grouped and m[0] != src and not (m[0] in wanter):
                                    print(f'appending {m[0]}')
                                    collection.append(m[0])
                                    lengths.append(len(m[1]))
                            if len(collection) >= 1:
                                selection = collection[lengths.index(min(lengths))]
                                print(f'selection --> {selection}')
                                status = True
                            else:
                                status = False

                            print(selection)
                            if status == True:
                                break


                        if status == False:
                            selection = randomly_choose()
        except ValueError:
            selection = randomly_choose()



        # print("appending: ", wanter[c])
        grouped.append(selection)
        group.append(selection)

    print("Grouped: ", group)
    groups.append(group)
print(groups)

