import random


def selDoubleTournament(individuals, k):
    chosen = []
    size = len(individuals)
    for i in range(k):
        p1, p2 = random.sample(range(size), 2)

        parents = [individuals[p1], individuals[p2]]
        # 选cost低的parent
        chosen.append(max(parents))
    return chosen


def orderedCorossover(ind1, ind2):
    path1 = getPathFromInd(ind1)
    path2 = getPathFromInd(ind2)
    length = len(path1)
    a, b = random.sample(range(length), 2)
    if a > b:
        a, b = b, a

    holes1 = set()
    holes2 = set()

    for i in range(a, b + 1):
        holes2.add(path1[i])
        holes2.add((path1[i][1], path1[i][0]))
        holes1.add(path2[i])
        holes1.add((path2[i][1], path2[i][0]))

    temp1, temp2 = path1.copy(), path2.copy()
    k1, k2 = b + 1, b + 1
    for i in range(length):
        if not temp1[(i + b + 1) % length] in holes1:
            path1[k1 % length] = temp1[(i + b + 1) % length]
            k1 += 1

        if not temp2[(i + b + 1) % length] in holes2:
            path2[k2 % length] = temp2[(i + b + 1) % length]
            k2 += 1

    # 交换选定序列里的元素
    for i in range(a, b + 1):
        path1[i], path2[i] = temp2[i], temp1[i]

    if random.random() > 0.5:
        return path1
    else:
        return path2


def getPathFromInd(ind):
    path = []
    for route in ind:
        # for node in route:
        path.extend(route)
    return path


def flip(c_path):
    posi = random.randint(0, len(c_path) - 1)
    c_path[posi] = (c_path[posi][1], c_path[posi][0])
    return c_path


def swap(c_path):
    r1, r2 = random.sample(range(len(c_path)), 2)
    temp = c_path[r1]
    c_path[r1] = c_path[r2]
    c_path[r2] = temp
    return c_path


def one(c_path: list):
    r1, r2 = random.sample(range(len(c_path)), 2)
    temp = c_path.pop(r1)
    if r1 > r2:
        c_path.insert(r2, temp)
    else:
        c_path.insert(r2 - 1, temp)
    return c_path


def two_opt(c_path: list):
    r1, r2 = random.sample(range(len(c_path)), 2)
    if r1 > r2:
        r1, r2 = r2, r1
    sub_path = c_path[r1: r2 + 1]
    sub_path.reverse()
    for i in range(len(sub_path)):
        sub_path[i] = (sub_path[i][1], sub_path[i][0])

    for i in range(r1, r2 + 1):
        c_path[i] = sub_path[i - r1]

    return c_path


def mutation(c_path):
    type = random.randint(1, 4)
    if type == 1:
        new_path = flip(c_path)
    elif type == 2:
        new_path = one(c_path)
    elif type == 3:
        new_path = two_opt(c_path)
    else:
        new_path = swap(c_path)

    return new_path
