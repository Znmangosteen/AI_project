import numpy as np
import random
import sys, time


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
                    if dist[i, a] < d:
                        d = dist[i, a]
                        u_next = u
                    elif dist[i, a] == d or (dist[i, a] < 0.9 * d and random.random() > 0.5):
                        judge = False
                        type = random.randint(1, 5)

                        if type == 1:
                            judge = better1(dist[u[0], depot], dist[u_next[0], depot])
                        elif type == 2:
                            judge = better2(dist[u[0], depot], dist[u_next[0], depot])
                        elif type == 3:
                            judge = better3(require_demand[u] / require_cost[u], require_demand[u] / require_cost[u])
                        elif type == 4:
                            judge = better4(require_demand[u] / require_cost[u], require_demand[u] / require_cost[u])
                        else:
                            judge = better5(dist[u[0], depot], dist[u_next[0], depot], load, capacity)

                        if judge:
                            u_next = u

            if u_next != ():
                if dist[i, depot] + dist[depot, u_next[0]] == dist[i, u_next[0]] and i != depot:
                    print('yes')
                    break
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


# 判断u是否比u_next好
def better1(u_dist, u_next_dist):
    return u_dist > u_next_dist


def better2(u_dist, u_next_dist):
    return u_dist < u_next_dist


def better3(u_rate, u_next_rate):
    return u_rate > u_next_rate


def better4(u_rate, u_next_rate):
    return u_rate < u_next_rate


def better5(u_dist, u_next_dist, load, capacity):
    is_better = u_dist > u_next_dist
    if load < (capacity / 2):
        return is_better
    else:
        return not is_better


if __name__ == '__main__':

    file_name = sys.argv[1]
    termination = sys.argv[3]
    random.seed(sys.argv[5])

    start_time = time.time()

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

    require_demand_copy = require_demand.copy()
    result = []
    cost = 1000000000000
    for aaa in range(500):
        result_t, cost_t = pathScanning()
        require_demand = require_demand_copy.copy()
        if cost_t < cost:
            result, cost = result_t, cost_t

    output_l1 = 's '
    route = str(result)[1:-1]
    route = route.replace(' ', '')
    output_l1 += route

    output_l2 = 'q ' + str(int(cost))
    print(output_l1)
    print(output_l2)

    # while True:
    #     time.sleep(0.2)
    #     if time.time()-start_time>int(termination):
    #         exit()
    #     else:
    #         print(time.time()-start_time)
