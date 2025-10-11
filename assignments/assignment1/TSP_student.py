#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 12:47:13 2022
Assignment 1: GA Template for TSP
@author: dgrimes
"""
import random
from TSP_Individual import *
import sys
import numpy as np
from scipy.spatial import distance_matrix
import pandas as pd 
from time import perf_counter
myStudentNum = 12345 # TODO Replace 12345 with your student number where R0002345 = 2345
random.seed(myStudentNum)

def genDists(fName):
    file = open(fName, 'r')
    size = int(file.readline())
    instance = {}
    for i in range(size):
        line=file.readline()
        (myid, x, y) = line.split()
        instance[int(myid)] = (int(x), int(y))
    file.close()
    dfcity= pd.DataFrame.from_dict(instance, orient="index")
    dfcity.rename(columns ={0:"x",1:"y"}, inplace = True)
    flt_dists = distance_matrix(dfcity.values,dfcity.values)
    return (np.rint(flt_dists)).astype(int)

class BasicTSP:
    def __init__(self, _fName, _maxIterations, _popSize, _xoverH, _xoverProb, _mutH, _mutationRate, _elites, _trunk, _dists):
        """
        Parameters and general variables
        Note not all parameters are currently used, it is up to you to implement how you wish to use them and where
        """

        self.population     = []
        self.matingPool     = []
        self.best           = None
        self.popSize        = int(_popSize)
        self.genSize        = None
        self.initH          = 0
        self.xoverH        = int(_xoverH)
        self.mutH        = int(_mutH)
        self.crossoverProb  = float(_xoverProb)
        self.mutationRate   = float(_mutationRate)
        self.maxIterations  = int(_maxIterations)
        self.fName          = _fName
        self.iteration      = 0
        self.data           = {}
        self.elites        = round(self.popSize * float(_elites))
        self.trunkSize = round(self.popSize * float(_trunk))
        self.dists           = _dists

        self.readInstance()
        self.bestInitSol = self.initPopulation()


    def readInstance(self):
        """
        Reading an instance from fName
        """
        file = open(self.fName, 'r')
        self.genSize = int(file.readline())
        self.data = {}
        for line in file:
            (cid, x, y) = line.split()
            self.data[int(cid)] = (int(x), int(y))
        file.close()

    def initPopulation(self):
        """
        Creating individuals in the initial population
        Either pure random tours (initH=0), or with insertion heuristic (initH=1)
        """
        for i in range(self.popSize):
            individual = Individual(self.genSize, self.data,self.initH, self.dists, [])
            if not(self.initH):
                individual.computeFitness()
            self.population.append(individual)

        self.best = self.population[0].copy()
        for ind_i in self.population:
            if self.best.getFitness() > ind_i.getFitness():
                self.best = ind_i.copy()
        return self.best.getFitness()

    def updateBest(self, candidate):
        if self.best == None or candidate.getFitness() < self.best.getFitness():
            self.best = candidate.copy()
    
    def randomSelection(self):
        """
        Random (uniform) selection of two individuals
        """
        indA = self.matingPool[ random.randint(0, self.trunkSize-1) ]
        indB = self.matingPool[ random.randint(0, self.trunkSize-1) ]
        return [indA, indB]
    
    def crossover(self, indA, indB):
        if random.random() > self.crossoverProb:
            child = Individual(self.genSize, self.data, 0, self.dists, random.choice([indA,indB]))
            return child
        elif self.xoverH == 0:
            return self.oxCrossover(indA, indB)
        else:
            return self.uniformCrossover(indA, indB)
        

    def oxCrossover(self, indA, indB):
        """
        Executes an ox crossover and returns the genes for a new individual
        """
        
        midP=random.randint(1, self.genSize-2)
        p1 =  indA[0:midP]
        genes = p1 + [i for i in indB if i not in p1]
        child = Individual(self.genSize, self.data, 0,self.dists, genes)
        return child

    def uniformCrossover(self, indA, indB):
        """
        Implement uniform crossover and returns the genes for a new individual
        """
        pass
    
    def mutation(self, ind):
        if random.random() > self.mutationRate:
            return
        elif self.mutH == 0:
            self.reciprocalMutation(ind)
        else:
            self.inversionMutation(ind)
    
    def reciprocalMutation(self, ind):
        """
        Mutate an individual by swapping two cities 
        """
        indexA = random.randint(0, self.genSize-1)
        indexB = random.randint(0, self.genSize-1)

        tmp = ind.genes[indexA]
        ind.genes[indexA] = ind.genes[indexB]
        ind.genes[indexB] = tmp
    
    def inversionMutation(self, ind):
        """
        Implement inversion mutation operator
        """
        pass

    def updateMatingPool(self):
        """
        Updating the mating pool for creating a new generation.
        Uses truncation selection to fill pool.
        Also computes elite solutions
        Note we are only storing the gene values and fitness of every 
        chromosome in prev pop
        """
        mybest = self.population[0:self.trunkSize]
        best_fits = [i.getFitness() for i in mybest]
        worst_fit=max(best_fits)
        worst_idx = best_fits.index(worst_fit)
        for i in range(self.trunkSize,self.popSize):
            if self.population[i].getFitness() < worst_fit:
                mybest[worst_idx] = self.population[i]
                best_fits[worst_idx] = self.population[i].getFitness()
                worst_fit = max(best_fits)
                worst_idx = best_fits.index(worst_fit)
                
        # Add copy of genes of each of the trunkSize best chromosomes in the old population
        self.matingPool = [[]+ind_i.genes for ind_i in mybest]
                
        ## Add truncation to mating pool, separately store elite best
        if self.elites < self.trunkSize:
            x = self.elites
        else:
            x = self.trunkSize
        elite_sols = mybest[0:x]
        if x:
            elite_fits = [i.getFitness() for i in elite_sols]
            worst_fit = max(elite_fits)
            worst_idx = elite_fits.index(worst_fit)
            for i in range(x,len(mybest)):
                if mybest[i].getFitness() < worst_fit:
                    elite_sols[worst_idx] = mybest[i]
                    elite_fits[worst_idx] = mybest[i].getFitness()
                    worst_fit = max(elite_fits)
                    worst_idx = elite_fits.index(worst_fit)
        return elite_sols


    def newGeneration(self):
        """
        Creating a new generation
        1. Selection
        2. Crossover
        3. Mutation
        """
        for i in range(self.elites, self.popSize):
            [ind1, ind2] = self.randomSelection() # select from mating pool
            child = self.crossover(ind1, ind2)
            self.mutation(child)
            child.computeFitness()
            self.updateBest(child)
            self.population[i] = child

    def GAStep(self):
        """
        One step in the GA main algorithm
        1. Updating mating pool with current population
        2. Creating a new Generation
        """

        elite_sols = self.updateMatingPool()
        # print()
        self.population[:self.elites] = elite_sols
        self.newGeneration()

    def search(self):
        """
        General search template.
        Iterates for a given number of steps
        """
        self.iteration = 0
        while self.iteration < self.maxIterations:
            self.GAStep()
            self.iteration += 1

        return self.best.getFitness(), self.bestInitSol, self.best.genes


def main():
    if len(sys.argv) < 10:
        print ("Error - Incorrect input")
        print ("Expecting python TSP.py [instance] [number of runs] [number of iterations] [population size]", 
                "[xover operator] [xover prob] [mutate operator] [mutate prob] [elitism] [truncation]")
        sys.exit(0)
    
    
    
    '''
    Reading in parameters, but it is up to you to implement what needs implementing
    TO DO:
    1/ Update myStudentNum variable to your student number (line 15 in this file)
    2/ Implement Uniform Crossover Operator
    3/ Implement Inversion Mutation Operator
    4/ Add code for metrics
    '''
    _, inst, nRuns, nIters, pop, xoverH, pC, mutH, pM, el, tr = sys.argv
    d = genDists(inst) # Get distance matrix
    nRuns = int(nRuns)
    
    # Perform 1st run (initialising metric variables)
    random.seed(myStudentNum) # Initialise seed
    ga = BasicTSP(inst, nIters, pop, xoverH, pC, mutH, pM, el, tr, d) # Create parameters
    bestDist, distInit, bestSol = ga.search()
    avgDist, avgInitDist = bestDist, distInit
    
    # Perform remaining runs
    for i in range(1,nRuns):
        random.seed(myStudentNum+i*100) # Update seed
        ga = BasicTSP(inst, nIters, pop, xoverH, pC, mutH, pM, el, tr, d)
        dist, distInit, sol = ga.search()
        avgDist += dist
        avgInitDist += distInit
        if dist < bestDist:
            bestDist = dist
            bestSol = sol
           
main()