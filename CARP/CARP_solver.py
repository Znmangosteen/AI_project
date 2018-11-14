import numpy as np
import random
import sys

# def pathScanning(depot, d, capacity, require_demand: dict,require_cost):
def pathScanning():
    s = []
    cost = 0
    while require_demand != {}:
        s.append(0)
        route = []
        i = depot
        load = 0

        d = 1000000000 - 1
        while require_demand != {} and d < 1000000000:
            d = 1000000000

            u_next = ()
            for u in require_demand:
                if load + require_demand[u] > capacity:
                    continue
                else:
                    a = u[0]
                    b = u[1]
                    if dist[i, a] < d:
                        d = dist[i, a]
                        u_next = u
                    elif dist[i, a] == d and better():
                        u_next = u

            if u_next != ():
                route.append(u_next)
                load += require_demand[u_next]
                cost += require_cost[u_next] + d
                require_demand.pop(u_next)
                require_demand.pop((u_next[1], u_next[0]))
                i = u_next[1]
        cost += dist[i, depot]
        s.extend(route)
        s.append(0)
    return s, cost


def better():
    return True


if __name__ == '__main__':
    # file_name = 'data/egl-e1-A.dat'
    # termination = 100
    # random.seed = 0
    file_name = sys.argv[1]
    termination = sys.argv[3]
    random.seed = sys.argv[5]
    # print(file_name)
    # print(termination)
    # print(random.seed)

    with open(file_name, 'r') as f:
        data = f.read().splitlines()

    vertices = int(data[1][11:])
    depot = int(data[2][8:])
    required_edge = int(data[3][17:])
    non_required_edge = int(data[4][21:])
    vehicles = int(data[5][11:])
    capacity = int(data[6][11:])
    total_cost_requ = int(data[7][31:])

    # print(vertices)
    # print(depot)
    # print(required_edge)
    # print(non_required_edge)
    # print(vehicles)
    # print(capacity)
    # print(total_cost_requ)

    dist = np.zeros((vertices + 1, vertices + 1), dtype='int64')
    for i in range(vertices + 1):
        for j in range(vertices + 1):
            dist[i, j] = 1000000000

    require_demand = {}
    require_cost = {}

    for i in data[9:-1]:
        line = i.split()
        a = int(line[0])
        b = int(line[1])
        cost = int(line[2])
        demand = int(line[3])

        dist[a, b] = cost
        dist[b, a] = cost

        if demand > 0:
            require_demand[(a, b)] = demand
            require_demand[(b, a)] = demand
            require_cost[(a, b)] = cost
            require_cost[(b, a)] = cost

    for k in range(vertices + 1):
        for i in range(vertices + 1):
            for j in range(vertices + 1):
                if i == j:
                    dist[i, j] = 0
                    continue
                if dist[i, k] + dist[k, j] < dist[i, j]:
                    dist[i, j] = dist[i, k] + dist[k, j]

    result, cost = pathScanning()

    output_l1 = 's '
    route = str(result)[1:-1]
    route = route.replace(' ', '')
    output_l1 += route

    output_l2 = 'q ' + str(int(cost))
    print(output_l1)
    print(output_l2)
