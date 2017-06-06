from DistanceTwoKeyPoints import search
from pylab import *


def Distance(init, goal, AREA_MAP):
    distance_between_two = search(AREA_MAP, init, goal)
    return distance_between_two


def TotalDistance(area, assignedArea, AREA_MAP):
    dist = 0
    for i in range(len(area) - 1):
        dist += Distance(assignedArea[area[i]], assignedArea[area[i + 1]], AREA_MAP)
        print "Distance between:", assignedArea[area[i]], assignedArea[area[i + 1]], " is ", Distance(
            assignedArea[area[i]], assignedArea[area[i + 1]], AREA_MAP)
    dist += Distance(assignedArea[area[-1]], assignedArea[area[0]], AREA_MAP)
    return dist


def reverse(area, n):
    nct = len(area)
    nn = (1 + ((n[1] - n[0]) % nct)) / 2
    for j in range(nn):
        k = (n[0] + j) % nct
        l = (n[1] - j) % nct
        (area[k], area[l]) = (area[l], area[k])  # swapping


keyPointsList = []


# -------------------- plotting without SA ------------------------------------------##
def withoutSA(area, assignedArea, distanceWithoutSA):
    keypoint = [assignedArea[area[i]] for i in range(len(area))]
    keypoint += [assignedArea[area[0]]]
    keypoint = array(keypoint)
    title('Total distance=' + str(distanceWithoutSA))
    keyPointsList = np.array(keypoint).tolist()
    print "-------Key Points List-----"
    print keyPointsList
    plot(keypoint[:, 0], keypoint[:, 1], '-o')
    # show()


# -------------------- plotting with SA ------------------------------------------##
def withSA(area, assignedArea, distanceWithoutSA, AREA_MAP, f_degree, b_degree, r_degree, l_degree, INTITAL_PLACE):
    keypoint = [assignedArea[area[i]] for i in range(len(area))]
    keypoint += [assignedArea[area[0]]]
    keypoint = array(keypoint)
    title('Total distance=' + str(distanceWithoutSA))
    keyPointsList = np.array(keypoint).tolist()
    plot(keypoint[:, 0], keypoint[:, 1], '-o')
    # show()
    print "--------- initial coverage order ---------"
    print keyPointsList

    # ------------------ setting the closest key point as start--------------------------- #
    cleanList = []
    [cleanList.append(x) for x in keyPointsList if x not in cleanList]
    keyPointsList = cleanList
    closestPoint = min(keyPointsList)
    closestPointIndex = keyPointsList.index(closestPoint)
    print "closestPointIndex: ", closestPointIndex
    newList = []
    for i in range(closestPointIndex):
        newList.append(keyPointsList[i])
    for i in range(closestPointIndex):
        keyPointsList.remove(keyPointsList[0])
    keyPointsList.extend(newList)

    keyPointsList.append(keyPointsList[0])
    print "--------- keyPoints coverage order  -------------"
    print keyPointsList

    # ------------------ setting the initial point--------------------------- #
    goal_init = keyPointsList
    print "Initial Goal---------", goal_init[0]

    from KeyPointsNavigation import draw as drawGui
    from KeyPointsNavigation import search as search

    # ------------------ Turtle GUI--------------------------- #
    drawGui(AREA_MAP, goal_init, len(AREA_MAP), len(AREA_MAP[0]), 10)

    # ------------------ take two key point and send as goal and init to move robot--------------------------- #
    for i in range(len(keyPointsList)):
        init = goal_init[i]
        goal = goal_init[i + 1]
        path_LocationList = search(init, goal, AREA_MAP, f_degree, b_degree, r_degree, l_degree)
        from CompassControl import key_input
        key_input(path_LocationList[0], f_degree, b_degree, r_degree, l_degree, INTITAL_PLACE, path_LocationList[1], AREA_MAP, assignedArea)

        goal_init.append(init)
        goal_init.append(goal)


def mainKeyPointCoverage(AREA_MAP, f_degree, b_degree, r_degree, l_degree, assignedArea, INTITAL_PLACE):
    print "AREA_MAP"
    for kr in range(len(AREA_MAP)):
        print AREA_MAP[kr]
    init = assignedArea[0]
    goal = assignedArea[1]
    print "init, goal: ", init, goal

    totalKeypoints = len(assignedArea)  # Number of cities to visit
    maxTsteps = 1  # Temperature is lowered not more than maxTsteps
    Tstart = 0.2  # Starting temperature - has to be high enough
    fCool = 0.9  # Factor to multiply temperature at each cooling step
    maxSteps = 10 * totalKeypoints  # Number of steps at constant temperature
    maxAccepted = 10 * totalKeypoints  # Number of accepted steps at constant temperature

    area = range(totalKeypoints)
    distanceWithoutSA = TotalDistance(area, assignedArea, AREA_MAP)  # Distance of the travel at without SA

    # Stores points of a move
    n = zeros(6, dtype=int)
    T = Tstart  # temperature

    # -------------------- plotting without SA ------------------------------------------##
    withoutSA(area, assignedArea, distanceWithoutSA)

    for t in range(maxTsteps):  # Over temperature
        accepted = 0
        for i in range(maxSteps):  # At each temperature, many Monte Carlo steps
            while True:  # Will find two random cities sufficiently close by
                # Two cities n[0] and n[1] are choosen at random
                n[0] = int((totalKeypoints) * rand())  # select one city
                n[1] = int((totalKeypoints - 1) * rand())  # select another city, but not the same
                if (n[1] >= n[0]):
                    n[1] += 1
                if (n[1] < n[0]):
                    (n[0], n[1]) = (n[1], n[0])  # swap, because it must be: n[0]<n[1]
                nn = (n[0] + totalKeypoints - n[
                    1] - 1) % totalKeypoints  # number of cities not on the segment n[0]..n[1]
                if nn >= 3: break

            # We want to have one index before and one after the two cities
            # The order hence is [n2,n0,n1,n3]
            n[2] = (n[0] - 1) % totalKeypoints  # index before n0
            n[3] = (n[1] + 1) % totalKeypoints  # index after n2

            # What would be the cost to reverse the path between city[n[0]]-city[n[1]]?
            de = Distance(assignedArea[area[n[2]]], assignedArea[area[n[1]]], AREA_MAP) + Distance(
                assignedArea[area[n[3]]], assignedArea[area[n[0]]],
                AREA_MAP) - Distance(
                assignedArea[area[n[2]]], assignedArea[area[n[0]]], AREA_MAP) - Distance(assignedArea[area[n[3]]],
                                                                                         assignedArea[area[n[1]]],
                                                                                         AREA_MAP)

            if de < 0 or exp(-de / T) > rand():  # Metropolis
                accepted += 1
                distanceWithoutSA += de
                reverse(area, n)

            if accepted > maxAccepted: break
        print "T=%10.5f , distance= %10.5f " % (T, distanceWithoutSA)
        T *= fCool  # The system is cooled down
        if accepted == 0: break  # If the path does not want to change any more, we can stop

    # -------------------- plotting with SA ------------------------------------------##
    withSA(area, assignedArea, distanceWithoutSA, AREA_MAP, f_degree, b_degree, r_degree, l_degree, INTITAL_PLACE)


if __name__ == '__main__':
    mainKeyPointCoverage()
