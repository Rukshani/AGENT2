import turtle
import time
from heuristicCalculation import heuristic_cal

delta = [[-1, 0],  # up
         [0, -1],  # left
         [1, 0],  # down
         [0, 1]]  # right

delta_name = ['^', '<', 'v', '>']

cost = 1
counter = 0

t = turtle.Pen()
dot_d = 20

new_list = []
RadiusOfWheel = 3.5


# currentLocation = []

# ------------------ Turtle GUI by dots--------------------------- #
def draw(grid, goal_init, rows, columns, speed):
    turtle.clear()
    turtle.reset()
    my_start = (goal_init[0][1] * dot_d, -goal_init[0][0] * dot_d)
    turtle.penup()
    turtle.setx(my_start[0])
    turtle.sety(my_start[1])
    turtle.pendown()

    t.clear()
    t.reset()
    t.penup()
    t.speed(speed)
    print "dot " + str(turtle.position())
    for i in range(rows):
        for j in range(columns):
            # for i in range(len(grid)):
            #     for j in range(len(grid[0])):
            if grid[i][j] == 1:
                t.dot(10, "blue")
                t.forward(dot_d)
            else:
                t.dot(10, "black")
                t.forward(dot_d)

        t.back(dot_d * (j + 1))
        t.right(90)
        t.forward(dot_d)
        t.left(90)


# ------------------ set initial point in Turtle GUI--------------------------- #
def set_initial(goal_init, turtle):
    my_start = (goal_init[0][1] * dot_d, -goal_init[0][0] * dot_d)
    turtle.penup()
    turtle.setx(my_start[0])
    turtle.sety(my_start[1])
    turtle.pendown()


def search(init, goal, grid, f_degree, b_degree, r_degree, l_degree):
    global gridGlobal, f_degreeGlobal, b_degreeGlobal, r_degreeGlobal, l_degreeGlobal
    gridGlobal = grid
    f_degreeGlobal = f_degree
    b_degreeGlobal = b_degree
    r_degreeGlobal = r_degree
    l_degreeGlobal = l_degree

    heuristic = heuristic_cal(grid)
    # turtle.speed(10)

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
    print "Init", init[0], init[1]
    print "Goal", x, y

    policy[x][y] = '*'
    pathList = []

    currentLocationList = []
    while x != init[0] or y != init[1]:
        # print "Current x, y: "+str(x)+" "+str(y)
        global currentLocation
        currentLocation = [x, y]
        currentLocationList.append(currentLocation)

        x2 = x - delta[action[x][y]][0]
        y2 = y - delta[action[x][y]][1]
        policy[x2][y2] = delta_name[action[x][y]]
        pathList.append(policy[x2][y2])
        x = x2
        y = y2

    for i in range(len(policy)):
        print policy[i]

    currentLocationList.append(init)
    currentLocationList.reverse()

    pathList.reverse()
    # print "Path List from", init, "to", goal, list
    print pathList
    new_list.append(pathList)
    # print "-----------alllist---------"
    # print new_list
    # print new_list[0]

    path_LocationList = [pathList, currentLocationList]

    for items in pathList:
        # time.sleep(1)
        turtle.setheading(90)
        if items == "^":
            turtle.setheading(90)
            turtle.forward(20)
            # print turtle.position()
        elif items == ">":
            turtle.setheading(90)
            turtle.right(90)
            turtle.forward(20)
            # turtle.forward(20)
            # print turtle.position()
        elif items == "<":
            turtle.setheading(90)
            turtle.left(90)
            turtle.forward(20)
            # print turtle.position()
        elif items == "v":
            turtle.setheading(90)
            turtle.left(90)
            turtle.left(90)
            turtle.forward(20)
            # print turtle.position()

            # print "-----------alllist---------"
            # print new_list
            # turtle.mainloop()

    return path_LocationList


def searchDetails(currentLocation, initialLocationPoint):
    search(currentLocation, initialLocationPoint, gridGlobal, f_degreeGlobal, b_degreeGlobal, r_degreeGlobal,
           l_degreeGlobal)
