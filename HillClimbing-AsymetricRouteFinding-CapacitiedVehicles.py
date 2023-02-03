import pandas as pd
import numpy as np
import math
import random
import time

# df_delivery= pd.read_csv("deneme_del.csv",index_col=[0],names=["Costumers", "Items"]).values
# df_distance= pd.read_csv("deneme_dist.csv",index_col=[0]).values
df_delivery= pd.read_csv("deliveries.csv",index_col=[0],names=["Costumers", "Items"]).values
df_distance= pd.read_csv("distances.csv",index_col=[0]).values


#definition of const values
num_vehicle = 2
#count of vehicle
capacity_vehicle = 900
# capacity of each vehicle
baseOf_Route = len(df_distance)-1
# route where does start from

# iterastion = int(math.factorial(len(df_distance)-1))
iterastion = 9999


def routeLength(data, result):
    routeLength = 0
    for i in range(len(result)):
        routeLength += data[result[i - 1]][result[i]]
        # sum of length of the all path

    return routeLength


def sumOfrouteLenght(Iterationroutes):
    sums = 0
    for i in range(len(Iterationroutes)):
        sums += Iterationroutes[i]['vehicleRouteLength']

    return sums

def capacityCheck(result):

    capacity = 0
    for i in range(len(result)):
        capacity += df_delivery[result[i]][0]

    return capacity

def isCapacityOkay(routes):

    capacityOkay = True
    for i in range(len(routes)):
        if(routes[i]['capacity'] > capacity_vehicle):
            capacityOkay = False


    return capacityOkay


def randomResult(data):
    # create random route
    result = []
    possibleCities = list(range(len(data)))
    routeCityCount = int((len(possibleCities) - 1) / num_vehicle)
    possibleCities.pop(baseOf_Route)

    for carCount in range(num_vehicle):
        appendenObject = {}
        appendenObject['vehicleId'] = carCount
        vehicleRoute = []
        vehicleRoute.append(baseOf_Route)
        for i in range(routeCityCount):
            randomCity = possibleCities[random.randint(0, len(possibleCities) - 1)]
            # pick random number in the numbers of cities
            vehicleRoute.append(randomCity)
            possibleCities.remove(randomCity)
            # by removing selectd random city, repeat prevented
        vehicleRoute.append(baseOf_Route)
        appendenObject['vehicleRandomRoute'] = vehicleRoute
        appendenObject['vehicleRouteLength'] = routeLength(data, appendenObject["vehicleRandomRoute"])
        appendenObject['capacity'] = capacityCheck(vehicleRoute)
        result.append(appendenObject)

    if (isCapacityOkay(result)):
        return result
    else:
        return randomResult(df_distance)


def neighbours(result):
    neighbour_lists = []
    for i in range(1, len(result) - 1):
        # It is start without changing start point "DEPOT"
        for j in range(i + 1, len(result) - 1):
            # It will end without changing end point "DEPOT"
            neighbour_Routes = result.copy()
            neighbour_Routes[i] = result[j]
            neighbour_Routes[j] = result[i]
            neighbour_lists.append(neighbour_Routes)

    return neighbour_lists


def getBestNeighbour(data, neighbour_list, currentPath, currentLenght):
    bestRouteLength = currentLenght
    bestNeighbour = currentPath

    for i in range(len(neighbour_list)):
        if (bestRouteLength > routeLength(data, neighbour_list[i])):
            bestRouteLength = routeLength(data, neighbour_list[i])
            bestNeighbour = neighbour_list[i]

    return bestNeighbour, bestRouteLength


def hillClimbing(data):
    currentSolution = randomResult(data)
    currentRouteLength = []
    neighbour_list = []

    # print(currentSolution)
    for i in range(len(currentSolution)):
        currentRouteLength.append(currentSolution[i]['vehicleRouteLength'])
        neighbour_list.append(neighbours(currentSolution[i]['vehicleRandomRoute']))

    for i in range(len(currentSolution)):
        bestNeighboursInfo = getBestNeighbour(data, neighbour_list[i], currentSolution[i]['vehicleRandomRoute'],
                                              currentSolution[i]['vehicleRouteLength'])
        currentSolution[i]['vehicleRandomRoute'] = bestNeighboursInfo[0]
        currentSolution[i]['vehicleRouteLength'] = bestNeighboursInfo[1]

    return currentSolution

if __name__ == "__main__":
    start_time = time.time()

    bestRoutesofAllIteration = repeatIteration(hillClimbing(df_distance))

    for i in range(len(bestRoutesofAllIteration[0])):
        print('\n Vehicle No: %s' %bestRoutesofAllIteration[0][i]['vehicleId'])
        print('-----------------------------')
        print('\n Vehicle Route: %s' %bestRoutesofAllIteration[0][i]['vehicleRandomRoute'])
        print('\n Vehicle Route Lenght: %s' %bestRoutesofAllIteration[0][i]['vehicleRouteLength'])
        print('\n Vehicle Vehicle Capacity: %s \n' %bestRoutesofAllIteration[0][i]['capacity'])

    print('All vehicle total route lenghts : %s' %bestRoutesofAllIteration[1])
    print('Iterastion Count : %s' %iterastion)
    print("Execution Time : --- %s seconds ---" % (time.time() - start_time))
