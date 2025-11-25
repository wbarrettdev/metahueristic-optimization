#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 19:07:48 2023

@author: dgrimes

Lab skeleton code
Fill in two functions with pass
Should also work on understanding the code

"""


import numpy as np
import time
import random
import sys
from os import listdir

random.seed(12345)
np.random.seed(12345)

class GSAT_solver:
    
    def __init__(self, file, _h, _wp, _maxFlips, _maxRestarts):
        self.maxFlips = _maxFlips
        self.maxRestarts = _maxRestarts
        self.flips = 0
        self.restarts = 0
        self.nVars, self.nClauses, self.clauses, self.litToClauses = -1,-1,[],{}
        self.readInstance(file)
        # nVars+1 in the following, instead of nVars, 
        # so that can index in from the variable names (which go from 1 to n instead of 0 to n-1)
        # i.e. never using index 0 of these arrays
        self.state = [0 for _ in range(self.nVars+1)]
        self.makecounts = np.zeros(self.nVars+1,dtype=int) # unsat that would go sat
        self.breakcounts = np.zeros(self.nVars+1,dtype=int) # sat that would go unsat
        self.bestObj = self.nClauses+1
        self.bestSol = [0 for _ in range(self.nVars)]
        self.wp = _wp
        self.h = _h

    def readInstance(self, fName):
        file        = open(fName, 'r')
        current_clause = []
        clauseInd = 0
    
        for line in file:
            data = line.split()
    
            if len(data) == 0:
                continue
            if data[0] == 'c':
                continue
            if data[0] == 'p':
                self.nVars  = int(data[2])
                self.nClauses    = int(data[3])
                
                continue
            if data[0] == '%':
                break
            if self.nVars == -1 or self.nClauses == -1:
                print ("Error, unexpected data")
                sys.exit(0)
    
            ##now data represents a clause
            for var_i in data:
                literal = int(var_i)
                if literal == 0:
                    self.clauses.append(current_clause)
                    current_clause = []
                    clauseInd += 1
                    continue
                current_clause.append(literal)
                if literal in self.litToClauses:
                    self.litToClauses[literal].add(clauseInd)
                else:
                    self.litToClauses[literal] = set([clauseInd])
                    
        for i in range(1,self.nVars+1):
            if i not in self.litToClauses:
                self.litToClauses[i] = set()
            if -i not in self.litToClauses:
                self.litToClauses[-i] = set()
                    
        if self.nClauses != len(self.clauses):
            print(self.nClauses, len(self.clauses))
            print ("Unexpected number of clauses in the problem")
            sys.exit(0)
        file.close()

    def generateSolution(self):
        for i in range(1, self.nVars+1):
            choice = [-1,1]
            self.state[i] = (i * random.choice(choice))

    def initial_cost(self):
        # Compute objective value of initial solution, reset counters and recompute
        self.unsat_clauses = set()
        self.obj = self.nClauses
        self.unsat_clauses = set()
        self.makecounts = np.zeros(self.nVars+1,dtype=int) # unsat that would go sat
        self.breakcounts = np.zeros(self.nVars+1,dtype=int) # sat that would go unsat
        self.breakcounts[0] = self.nClauses+1
        num_unsat = 0
        clsInd = 0
        for clause in self.clauses:
            satLits = 0
            breakV = 0
            cStatus = False
            for lit in clause:
                if lit in self.state:
                    cStatus = True
                    satLits += 1
                    breakV = lit
                if satLits > 1:
                    break
            if satLits == 1:
                self.breakcounts[abs(breakV)] += 1
            if not cStatus:
                num_unsat += 1
                self.unsat_clauses.add(clsInd)
                for lit in clause:
                    self.makecounts[abs(lit)] += 1
            clsInd += 1
        self.obj = num_unsat
        if self.bestObj == -1:
            self.bestObj = num_unsat
            self.bestSol = self.state[1:]
        # print("Initial cost", self.obj) #,"\tTest",np.sum(self.makecounts))
        # print(self.breakcounts,self.makecounts,"\n",sep="\n")

    def flip(self, variable):
        self.flips += 1
        self.state[variable] *= -1
        self.update_counts(variable)

    # Function to update objective value, counts of variables and list of currently unsat_clauses
    # Run after flipping 
    def update_counts(self, variable):
        # Clauses unsat involving variable
        # Decrement the makecount for all variables in clauses going unsat to sat
        # Increment the breakcount of flipped variable for each such clause (since it is the only satisfying literal of it)
        # Clauses sat involving variable where literal is now false
        # If clause now unsat: increment the makecount for all variables in the clause
        # If clause still sat: then need to check if only 1 var satisfying it and increment breakcount of that var if so
        # Clauses sat involving variable where literal is now true:
        # If clause had only one satisfying literal previously, now it has 2, and so need to decrement the breakcount of this other var
        pass

    def selectVar(self):
        if self.h =="gsat":
            return self.selectGSATvar()

    # Fill in variable selection
    def selectGSATvar(self):
        pass
    
    def solve(self):
        # startT =  time.time()
        # self.initialize()
        self.restarts = 0
        while self.restarts < self.maxRestarts and self.bestObj > 0:
            self.restarts += 1
            self.generateSolution()
            self.initial_cost()
            self.flips = 0
            while self.flips < self.maxFlips and self.bestObj > 0:
                nextvar = self.selectVar()
                self.flip(nextvar)
                if self.obj < self.bestObj:
                    self.bestObj = self.obj
                    self.bestSol = self.state[1:]

        if self.bestObj == 0:
        #     # print("SAT")
        #     # print("Sol:\n",self.bestSol)
            solutionChecker(self.clauses, self.bestSol)
        # else:
        #     # print("Best obj", self.bestObj, "\n"*3)
        #     solutionChecker(self.clauses, self.bestSol)
        return self.flips, self.restarts, self.bestObj

def solutionChecker(clauses, sol):
    # startPython = (round(time.time() * 1000, 2))
    unsat_clause = 0
    for clause in clauses:
        cStatus = False
        for var in clause:
            if var in sol:
                cStatus = True
                break
        if not cStatus:
            unsat_clause+=1
    # stopPython = (round(time.time() * 1000,2))
    # print("t4",stopPython-startPython)
    if unsat_clause > 0:
        print ("UNSAT Clauses: ",unsat_clause)
        return False
    return True



def main():
    if len(sys.argv) < 8:
        print(len(sys.argv))
        print ("Error - Incorrect input")
        print ("Expecting python gsat.py [fileDir] [alg] [number of runs] [max restarts]",
               "[max flips] [walk prob] [studentNum]")
        sys.exit(0)

    _, filesDir, alg, nRuns, maxRes, maxFlips, wp, sNum  = sys.argv

    lastNum = sNum[-1]
    sNum, nRuns, maxRes, maxFlips, wp = int(sNum), int(nRuns), int(maxRes), int(maxFlips), float(wp)
    # directory = "Inst/uf75-325" #50-218"

    # Iterate through all instances in the directory that end with 
    # last value of your student number 
    
    for filename in listdir(filesDir):
        if filename.endswith("03.cnf"):
        # if filename.endswith(lastNum+".cnf"):
            satInst=filesDir+"/"+filename

            avgRestarts, avgFlips, avgUnsatC, avgTime, unsolved = 0, 0, 0, 0, 0

            for i in range(nRuns):
                # print("Run",i+1, end="\t")
                random.seed(sNum + i*100)
                gsat = GSAT_solver(satInst, alg, wp, maxFlips, maxRes)
                startPython = time.process_time()
                ctrFlips, ctrRestarts, ctrObj = gsat.solve()
                stopPython = time.process_time() #(round(time.time() * 1000,2))
                avgFlips += ctrFlips
                avgRestarts += ctrRestarts
                avgUnsatC += ctrObj
                avgTime += (stopPython-startPython)
                if ctrObj > 0:
                    unsolved += 1
             
            print(filename, "Solved:",nRuns - unsolved, "\tAvg Obj:",avgUnsatC/nRuns, 
                  "\tAvg Restarts:",avgRestarts/nRuns, "\tAvg Flips:",avgFlips/nRuns, 
                  "\tAvg Time:",avgTime/nRuns)
            
main()
