from heuristicCalculation import heuristic_cal

delta = [[-1, 0], [0, -1], [1, 0], [0, 1]]

delta_name = ['^', '<', 'v', '>']
cost = 1


def search(grid, init, goal):
    heuristic = heuristic_cal(grid)
    closed = [[0 for row in range(len(grid[0]))] for col in range(len(grid))]
    closed[init[0]][init[1]] = 1
    action = [[-1 for row in range(len(grid[0]))] for col in range(len(grid))]
    policy = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]

    x = init[0]
    y = init[1]
    g = 0
    h = heuristic[x][y]
    f = g + h

    open = [[f, g, h, x, y]]

    found = False
    resign = False

    while found is False and resign is False:
        if len(open) == 0:
            resign = True
            print 'fail'
        else:
            open.sort()
            open.reverse()
            next = open.pop()
            x = next[3]
            y = next[4]
            g = next[1]

            if x == goal[0] and y == goal[1]:
                found = True
            else:
                for i in range(len(delta)):
                    x2 = x + delta[i][0]
                    y2 = y + delta[i][1]
                    if 0 <= x2 < len(grid) and 0 <= y2 < len(grid[0]):
                        if closed[x2][y2] == 0 and grid[x2][y2] == 0:
                            g2 = g + cost
                            h2 = heuristic[x2][y2]
                            f2 = g2 + h2
                            open.append([f2, g2, h2, x2, y2])
                            closed[x2][y2] = 1
                            action[x2][y2] = i

    x = goal[0]
    y = goal[1]

    policy[x][y] = '*'
    list = []
    while x != init[0] or y != init[1]:
        x2 = x - delta[action[x][y]][0]
        y2 = y - delta[action[x][y]][1]
        policy[x2][y2] = delta_name[action[x][y]]
        list.append(policy[x2][y2])
        x = x2
        y = y2

    # for i in range(len(policy)):
    #     print policy[i]

    list.reverse()
    list.append(list[-1])
    return len(list) - 1
