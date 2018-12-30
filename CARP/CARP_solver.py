import numpy as np
import random
import sys, time
from path_class import path
import GA


# def pathScanning(depot, d, capacity, require_demand: dict,require_cost):
def pathScanning():
    s = []
    cost = 0
    type = random.randint(1, 6)

    while require_demand != {}:
        # s.append(0)
        route = []
        i = depot
        load = 0
        break_rate = random.randint(10, 25)
        rate = capacity * 0.91

        d = 1000000000 - 1
        # 找一条路
        while require_demand != {} and d < 1000000000:
            d = 1000000000

            # if random.random() < load / (capacity * break_rate):
            #     break

            u_next = ()
            # 找下一个节点
            for u in require_demand:
                if load + require_demand[u] > capacity:
                    continue
                # elif u_next != () and random.random() < 1 / 10000:
                #     break
                else:
                    a = u[0]
                    temp_dist = dist[i, a]
                    if load > rate and will_break:
                        back_dist = dist[i, 1]
                        fin_back_dist = dist[u[1], 1]
                        s_cost = require_cost[u]
                        if temp_dist + s_cost + fin_back_dist > back_dist:
                            continue

                    if dist[i, a] < d:
                        d = dist[i, a]
                        u_next = u
                    elif dist[i, a] == d or (98 * dist[i, a] < 100 * d and random.random() > 0.98):
                        judge = False

                        if type == 1:
                            judge = better1(dist[u[0], depot], dist[u_next[0], depot])
                            # judge = better5(dist[u[0], depot], dist[u_next[0], depot], load, capacity)

                        elif type == 2:
                            judge = better2(dist[u[0], depot], dist[u_next[0], depot])
                            # judge = better5(dist[u[0], depot], dist[u_next[0], depot], load, capacity)

                        elif type == 3:
                            judge = better3(require_demand[u] / require_cost[u], require_demand[u] / require_cost[u])
                        elif type == 4:
                            judge = better4(require_demand[u] / require_cost[u], require_demand[u] / require_cost[u])
                        elif type == 5:
                            judge = better5(dist[u[0], depot], dist[u_next[0], depot], load, capacity)
                        else:
                            judge = (random.random() > 0.5)

                        if judge:
                            u_next = u

            if u_next != ():
                if i != depot and u_next[0] != depot and dist[i, u_next[0]] == dist[i, depot] + dist[depot, u_next[0]]:
                    break
                # if dist[i, depot] + dist[depot, u_next[0]] == dist[i, u_next[0]] and i != depot:
                #     # print('yes')
                #     break

                route.append(u_next)
                # route += [u_next]
                load += require_demand[u_next]
                cost += require_cost[u_next] + d
                require_demand.pop(u_next)
                require_demand.pop((u_next[1], u_next[0]))
                i = u_next[1]
        cost += dist[i, depot]
        s.append(route)
        # s += [route]
        # s.append(0)
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


def ulusoy(path):
    path = [(0, 0)] + path
    length = len(path)

    V = [1000000000 for i in range(length)]
    P = [1000 for i in range(length)]
    P[0] = 0
    V[0] = 0

    for i in range(1, length):
        load = 0
        cost = 0
        j = i
        while j < length and load < capacity:
            load += require_demand_copy[path[j]]
            if i == j:
                cost = dist[1, path[i][0]] + require_cost[path[i]] + dist[path[i][1], 1]
            else:
                cost = cost - dist[path[j - 1][1], 1] + dist[path[j - 1][1], path[j][0]] + require_cost[path[j]] + dist[
                    path[j][1], 1]
            if load <= capacity:
                if V[i - 1] + cost < V[j]:
                    V[j] = V[i - 1] + cost
                    P[j] = i - 1
                j += 1

    comp_path = []

    i = length - 1
    while i > 0:
        last_route_end = P[i]
        route_start = last_route_end + 1
        route = []
        for j in range(route_start, i + 1):
            route.append(path[j])
        comp_path.append(route)
        i = last_route_end

    return comp_path, V[length - 1]


def cal(p):
    path = p
    cost = 0
    for route in path:
        cost += dist[route[0][0], 1] + dist[route[-1][1], 1]
        for i in range(len(route) - 1):
            cost += dist[route[i][1], route[i + 1][0]]

    cost += total_cost_requ
    return cost


# 输出函数
def s_format(s):
    s_print = []
    for p in s:
        s_print.append(0)
        s_print.extend(p)
        s_print.append(0)
    return s_print


if __name__ == '__main__':

    file_name = sys.argv[1]
    termination = sys.argv[3]
    # random.seed(sys.argv[5])

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

    total_demand = 0
    # shuffles = [[], [], [], []]

    for i in data[9:-1]:
        line = i.split()
        a = int(line[0])
        b = int(line[1])
        cost = int(line[2])
        demand = int(line[3])

        dist[a, b] = cost
        dist[b, a] = cost

        if demand > 0:
            total_demand += demand
            require_demand[(a, b)] = demand
            require_demand[(b, a)] = demand
            require_cost[(a, b)] = cost
            require_cost[(b, a)] = cost
            # if random.random() > 0.5:
            #     shuffles[0].append((a, b))
            #     shuffles[1].append((a, b))
            #     shuffles[2].append((b, a))
            #     shuffles[3].append((b, a))
            # else:
            #     shuffles[0].append((b, a))
            #     shuffles[1].append((b, a))
            #     shuffles[2].append((a, b))
            #     shuffles[3].append((a, b))

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
    population = []
    exit_cost = set()
    population_size = 5500
    will_break = (capacity < total_demand)

    while len(population) < population_size:
        result_t, cost_t = pathScanning()
        # if not cost_t in exit_cost:
        # if cost in exit_cost:
        #     p_path = random.shuffle(shuffles[random.randint(0, 3)])
        #     result_t, cost_t = ulusoy(p_path)
        #     population.append(path(result_t, cost_t))
        #     exit_cost.add(cost_t)
        # else:
        #     exit_cost.add(cost_t)
        population.append(path(result_t, cost_t))

        require_demand = require_demand_copy.copy()

    population.sort()
    print(time.time() - start_time)

    # GA part
    pm = 0.001
    gen = 0
    # for i in range(10000):
    while True:
        gen += 1
        if time.time() - start_time > int(termination) - 3:
            break
        parents = GA.selDoubleTournament(population, 2)
        child_path = GA.orderedCorossover(parents[0].p, parents[1].p)
        result_t, cost_t = ulusoy(child_path)

        child = path(result_t, cost_t)
        # population.append(child)

        if random.random() < pm:
            s = GA.mutation(child_path)
            result_t, cost_t = ulusoy(s)
            # if cost not in exit_cost:
            child = path(result_t, cost_t)

        # if child.cost not in exit_cost:
        replace = random.randint(0, population_size / 2)
        population[replace] = child
        exit_cost.add(child.cost)
        population.sort()

    # output_l1 = 's '
    # route = str(result)[1:-1]
    # route = route.replace(' ', '')
    # output_l1 += route
    #
    # print(output_l1)
    # print(gen)
    result, cost = population[-1].p, population[-1].cost
    # co_cost = cal(result)
    # print(co_cost)
    print("s", (",".join(str(d) for d in s_format(result))).replace(" ", ""))
    output_l2 = 'q ' + str(int(cost))
    print(output_l2)
    print(time.time() - start_time)
    # while True:
    #     time.sleep(0.2)
    #     if time.time()-start_time>int(termination):
    #         exit()
    #     else:
    #         print(time.time()-start_time)
