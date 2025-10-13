#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 23:36:17 2024

Author: Diarmuid Grimes, based on code of Alejandro Arbelaez
Heuristics for quickly generating (non-optimal) solution to TSP
File contains two heuristics. 
First heuristic is the well-known nearest neighbor heuristic: inserts the closest unrouted city to the previous city 
added to the route.
Second heuristic inserts randomly chosen unrouted city directly after its 
nearest city on the route
file: Lab1_TSP.py
Usage: python Lab1_TSP.py dataset nRuns
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

# 
# Read instance in tsp format
def readInstance(fName):
    file = open(fName, 'r')
    size = int(file.readline())
    inst = {}
    for i in range(size):
        line=file.readline()
        (myid, x, y) = line.split()
        inst[int(myid)-1] = (int(x), int(y))
    file.close()
    return inst

# Compute Euclidean distance between pair of (x,y) coords
def euclideanDistance(cityA, cityB):
    #return sqrt( (cityA[0]-cityB[0])**2 + (cityA[1]-cityB[1])**2 )
    ##Rounding nearest integer
    return round( sqrt( (cityA[0]-cityB[0])**2 + (cityA[1]-cityB[1])**2 ) )


# If doing multiple runs may be better to compute all distances once
# and store for lookup in each run 
def genDists(instance):
    cities=list(instance.keys())
    nCities=len(cities)
    dists= np.zeros((nCities,nCities),dtype=int)
    for i in range(nCities):
        for j in range(nCities):
            dists[i][j]=dists[j][i]=euclideanDistance(instance[cities[i]], instance[cities[j]])
    return dists 

# Same as gendists but uses scipy function to compute distance matrix    
def genDists2(instance):
    dfcity= pd.DataFrame.from_dict(instance, orient="index")
    dfcity.rename(columns ={0:"x",1:"y"}, inplace = True)
    flt_dists = distance_matrix(dfcity.values,dfcity.values)
    return (np.rint(flt_dists)).astype(int)

def saveSolution(fName, inst, alg, cost, solution):
    file = open(fName, 'a')
    file.write(inst+"\t"+alg+"\t"+str(cost)+"\t\t")
    for city in solution:
        file.write(str(city)+" ")
    file.write("\n")
    file.close()


def compareDistanceMatrixMethods():
    directory = "TSPdataset"
    print("\t","Basic","Scipy",sep="\t")
    for filename in listdir(directory):
        if filename.endswith(".tsp") and filename.startswith("inst"):
            tspInst=readInstance(directory+"/"+filename)
            basicTime = 0
            spatialTime = 0
            for i in range(100): 
                s = time.process_time()
                genDists(tspInst)
                e = time.process_time()
                genDists2(tspInst)
                e2 = time.process_time()
                basicTime += e-s
                spatialTime += e2-e
            print(filename,basicTime,spatialTime,sep="\t")

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

    # a_scale = float(max(x))/float(100)
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


# Heuristics 
#
# Choose first city randomly, thereafter append nearest unrouted city to last city added to route
# cities variable
def nearestNeighbor(instance):
    unvisited = list(instance.keys())
    tCost = 0

    # Randomly choose a city to start the tour
    cIndex = random.randint(0, len(instance)-1)
    tour = [unvisited[cIndex]] #Initialise tour to this city
    del unvisited[cIndex] # Remove from unvisited
    current_city = tour[0] # This variable will store the last city added to the tour in each iteration

    while len(unvisited) > 0:
        # initialise the distance (bcost) to first unvisited city
        bCity = unvisited[0]
        bCost = euclideanDistance(instance[current_city], instance[bCity])
        bIndex = 0
        #Then iterate through remaining unvisited cities to see if there is a nearer city
        for city_index in range(1, len(unvisited)):
            city = unvisited[city_index]
            cost = euclideanDistance(instance[current_city], instance[city])

            if bCost > cost:
                bCost = cost
                bIndex = city_index
        tCost += bCost                          # Update tour cost
        current_city = unvisited[bIndex]        # Update current city to new city chosen
        tour.append(current_city)
        del unvisited[bIndex]

    # Add distance from ginal city back to first city    
    tCost += euclideanDistance(instance[tour[-1]], instance[tour[0]])

    return tour, tCost


# Same as heuristic 1 but distances are precomputed so much faster if doing multiple runs
def nearestNeighborPrecomp(instance, distances):
    unvisited = list(instance.keys())
    cIndex = random.randint(0, len(instance)-1)
    tCost = 0
    tour = [unvisited[cIndex]]   
    del unvisited[cIndex]
    current_city = tour[0]
    while len(unvisited) > 0:
        bCity = unvisited[0]
        bCost = distances[current_city][bCity]
        bIndex = 0
        for city_index in range(1, len(unvisited)):
            city = unvisited[city_index]
            cost = distances[current_city][city] 

            if bCost > cost:
                bCost = cost
                bCity = city
                bIndex = city_index
        tCost += bCost
        current_city = bCity
        tour.append(current_city)
        del unvisited[bIndex]
    tCost += distances[current_city][tour[0]] 
    return tour, tCost

# Choose unrouted city randomly, insert into route after nearest routed city 
def alternativeHeuristic(instance, distances):
    unvisited = list(instance.keys())
    nCities=len(unvisited)
    # Choose first two cities randomly
    cIndex, cIndex1 = random.sample(range(0, len(instance)-1),2)
    tCost = 0
    tour = [unvisited[cIndex], unvisited[cIndex1]]
    del unvisited[cIndex]
    del unvisited[cIndex1]

    while len(unvisited) > 0:
        cIndex = random.randint(0, len(unvisited)-1)
        nextCity = unvisited[cIndex]
        del unvisited[cIndex]
        bCost = distances[tour[0]][nextCity] # initialise bCost
        bIndex = 0
        for city_index in range(1, len(tour)):
            city = tour[city_index]
            cost = distances[city][nextCity]
            if bCost > cost:
                bCost = cost
                bIndex = city_index
        # Insert after nearest city
        tour.insert(bIndex+1, nextCity)
    for i in range(nCities):
        tCost += distances[tour[i]][tour[(i+1)%nCities]]
    return tour, tCost    


def randomTours(instance):
    tour=list(instance.keys())
    random.shuffle(tour)
    nCities=len(tour)
    tCost=0
    for i in range(nCities):
        tCost+=euclideanDistance(instance[tour[i]], instance[tour[(i+1)%nCities]])
    return tour, tCost 

def randomToursPrecomp(instance, distance):
    cities=list(instance.keys())
    random.shuffle(cities)
    nCities=len(cities)
    tCost=0
    for i in range(nCities):
        tCost+=distance[cities[i]][cities[(i+1)%nCities]]
    return cities, tCost 



def main():
    directory = "TSPdataset" #sys.argv[1]
    if len(sys.argv)>2: # Default is 100 runs
        runs = int(sys.argv[2])
    else:
        runs = 10
    if len(sys.argv)>3: # Default is 100 runs
        output = sys.argv[3]
    else:
        output = 0
        
        

    # Iterate through all tsp instances in the directory
    for filename in listdir(directory):
        if filename.endswith(".tsp") and filename.startswith("i"):
            sNum = 12345 # Initial random seed value
            tspInst=readInstance(directory+"/"+filename)
            # Generate Distances
            
            # Compared 2 approaches, one basic (genDists), one Scipy (genDists2)
            # Scipy orders of magnitude faster so commented out other
            # print("\n",filename)
            
            # startTime = round(time.time(), 4)
            # dists = genDists(tspInst)
            # stopTime = round(time.time(), 4)
            # distMatrixTimeBasic = (stopTime - startTime)
            # print("Basic:",distMatrixTimeBasic)

            startTime = round(time.time(), 4)
            dists = genDists2(tspInst)
            stopTime = round(time.time(), 4)
            distMatrixTimeScipy = (stopTime - startTime)           
            # print("Scipy:",distMatrixTimeScipy)
            # continue

            random.seed(sNum)
            startTime = round(time.time(),4)
            # Run once outside of loop to initialise counters minCost and avg Cost
            solution = nearestNeighbor(tspInst)
            h1minCost, avgCost, bestSol = solution[1], solution[1], solution[0]
            for i in range(1,runs):
                random.seed(sNum + i*100)
                solution = nearestNeighbor(tspInst)
                avgCost += solution[1]
                if(solution[1]<h1minCost):
                    h1minCost, bestSol = solution[1], solution[0]
            stopTime = round(time.time(),4)
            # print(solution[0])
            # plotSol(tspInst, bestSol)
            h1Cost = avgCost/runs
            h1Time = (stopTime - startTime)
            if output:
                saveSolution(output, filename,"NN",h1minCost, bestSol)
            
            # Run alternative heuristic
            startTime = round(time.time(),4)
            random.seed(12345)
            solution = alternativeHeuristic(tspInst, dists)
            h2minCost, avgCost, bestSol = solution[1], solution[1], solution[0]
            for i in range(1,runs):
                solution = alternativeHeuristic(tspInst, dists)
                avgCost += solution[1]
                if(solution[1]<h2minCost):
                    h2minCost, bestSol = solution[1], solution[0]
            stopTime = round(time.time(),4)
            h2Cost = avgCost/runs
            h2Time = (stopTime - startTime)
            # plotSol(tspInst, bestSol)
            if output:
                saveSolution(output, filename,"Alt",h2minCost, bestSol)
                
            startTime = round(time.time(),4)
            random.seed(12345)
            solution = randomToursPrecomp(tspInst, dists)
            rminCost, avgCost, bestSol = solution[1], solution[1], solution[0]
            for i in range(1,runs):
                solution = randomTours(tspInst)
                avgCost += solution[1]
                if(solution[1]<rminCost):
                    rminCost, bestSol = solution[1], solution[0]
            stopTime = round(time.time(),4)
            rCost = avgCost/runs
            rTime = (stopTime - startTime)
            # plotSol(tspInst, bestSol)
            if output:
                saveSolution(output, filename,"Rand",h2minCost, bestSol)
                
            print(filename,"\t",h1Cost,h2Cost,rCost,"\t",h1minCost,h2minCost,rminCost,"\t",
                        round(h1Time,3),round(h2Time,3),round(rTime,3),round(distMatrixTimeScipy,3))


    
main()





