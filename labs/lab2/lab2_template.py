"""
Author: Diarmuid Grimes, based on code of Alejandro Arbelaez
Lab tempalte
file: lab2_template.py
"""

import random
import sys
import time
from os import listdir
from math import sqrt
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
from scipy.spatial import distance_matrix
 
# Read instance in tsp format
def readInstance(fName):
    file = open(fName, 'r')
    size = int(file.readline())
    inst = {}
    for i in range(size):
        line=file.readline()
        (myid, x, y) = line.split()
        inst[int(myid)] = (int(x), int(y))
    file.close()
    return inst

# Compute Euclidean distance between pair of (x,y) coords
def euclideanDistance(cityA, cityB):
    #return sqrt( (cityA[0]-cityB[0])**2 + (cityA[1]-cityB[1])**2 )
    ##Rounding nearest integer
    return round( sqrt( (cityA[0]-cityB[0])**2 + (cityA[1]-cityB[1])**2 ) )


def saveSolution(fName, solution, cost):
    file = open(fName, 'w')
    file.write(str(cost)+"\n")
    for city in solution:
        file.write(str(city)+"\n")
    file.close()


"""
Implement the following heuristics:
1/ nearest neighbor
2/ alt insertion
3/ random 
"""

'''
Nearest Neighbor
Choose first city randomly and add it to the tour, thereafter append 
the unvisited city that is nearest to the last city added to route
'''
def nearest_neighbor(instance):
    unvisited = list(instance.keys()) # Keep track of currently unvisited cities
    tCost = 0 # Cost of tour

    # Randomly choose a city to start the tour
    cIndex = random.randint(0, len(instance)-1)
    tour = [unvisited[cIndex]] #Initialise tour to this city
    del unvisited[cIndex] # Remove from unvisited
    current_city = tour[0] # This variable will store the last city added to the tour in each iteration

    while len(unvisited) > 0:
        # INSERT CODE HERE
        print("Insert code here!")

    return tour, tCost

# Choose first two cities randomly
# Iterate through unvisited and insert it to the right of the nearest 
# city on the current tour
def alt_insertion(instance):
    unvisited = list(instance.keys())
    tCost = 0

    # Randomly choose a city to start the tour
    cIndex = random.randint(0, len(instance)-1)
    tour = [unvisited[cIndex]] #Initialise tour to this city
    del unvisited[cIndex] # Remove from unvisited
    current_city = tour[0] # This variable will store the last city added to the tour in each iteration

    while len(unvisited) > 0:
        # INSERT CODE HERE
        print("Insert code here!")

    return tour, tCost

def randomTours(instance):
    pass


# Visualise tour 
# Based on https://gist.github.com/payoung/6087046
def plotSol(inst,sol):
    x = []; y = []
    for i in sol:
        x.append(inst[i][0])
        y.append(inst[i][1])
    # plt.plot(x, y, 'co')
    plt.plot(x[0],y[0],'r^')
    plt.plot(x[-1],y[-1],'bv')

    x.append(inst[sol[0]][0]), y.append(inst[sol[0]][1])
    plt.plot(x,y)

    a_scale = float(max(x))/float(100)
    # Draw the primary path for the TSP problem
    

    # plt.arrow(x[-1], y[-1], (x[0] - x[-1]), (y[0] - y[-1]), head_width = a_scale, 
    # color ='g', length_includes_head=True)
    # for i in range(0,len(x)-1):
    #     plt.arrow(x[i], y[i], (x[i+1] - x[i]), (y[i+1] - y[i]), head_width = a_scale,
    #               color = 'g', length_includes_head = True)

    #Set axis to slightly larger than the set of x and y
    plt.xlim(min(x)*0.95, max(x)*1.01)
    plt.ylim(min(y)*0.95, max(y)*1.01)
    plt.show()



def main():
    directory = sys.argv[1]
    output = sys.argv[2]
    if len(sys.argv)>3: # Default is 100 runs
        runs = int(sys.argv[3])
    else:
        runs = 100

    # print("Alg","Inst\t", "Best Obj","Avg Obj\t", "Total Time", sep="\t")
    # Iterate through all tsp instances in the directory
    for filename in listdir(directory):
        if filename.endswith(".tsp"):
            tspInst=readInstance(directory+"/"+filename)
            startTime = int(round(time.time() * 1000))
            random.seed(12345)
            # Run once outside of loop to initialise counters minCost and avg Cost
            solution = nearest_neighbor(tspInst)
            minCost, avgCost, bestsol = solution[1], solution[1], solution[0]
            for i in range(1,runs):
                solution = nearest_neighbor(tspInst)
                avgCost += solution[1]
                # print(solution[1])
                if(solution[1]<minCost):
                    minCost, bestsol = solution[1], solution[0]
            stopTime = int(round(time.time() * 1000))
            # print(solution[0])
            # plotSol(tspInst, bestsol)
            avgCost /= runs
            runTime = (stopTime - startTime)/runs
            print("NN",minCost, avgCost, runTime)
            

            startTime = int(round(time.time() * 1000))
            random.seed(12345)
            # Run once outside of loop to initialise counters minCost and avg Cost
            solution = alt_insertion(tspInst)
            minCost, avgCost, bestsol = solution[1], solution[1], solution[0]
            for i in range(1,runs):
                solution = alt_insertion(tspInst)
                avgCost += solution[1]
                # print(solution[1])
                if(solution[1]<minCost):
                    minCost, bestsol = solution[1], solution[0]
            stopTime = int(round(time.time() * 1000))
            # print(solution[0])
            # plotSol(tspInst, bestsol)
            avgCost /= runs
            runTime = (stopTime - startTime)/runs
            print("Alt Insertion",minCost, avgCost, runTime)

            startTime = int(round(time.time() * 1000))
            random.seed(12345)
            # Run once outside of loop to initialise counters minCost and avg Cost
            solution = randomTours(tspInst)
            minCost, avgCost, bestsol = solution[1], solution[1], solution[0]
            for i in range(1,runs):
                solution = randomTours(tspInst)
                avgCost += solution[1]
                # print(solution[1])
                if(solution[1]<minCost):
                    minCost, bestsol = solution[1], solution[0]
            stopTime = int(round(time.time() * 1000))
            # print(solution[0])
            # plotSol(tspInst, bestsol)
            avgCost /= runs
            runTime = (stopTime - startTime)/runs
            print("Random",minCost, avgCost, runTime)


    
main()





