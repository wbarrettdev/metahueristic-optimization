#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 24 21:04 2025

@author: wbarrett
"""

import numpy as np
from time import perf_counter
import random
import sys
from os import listdir
myStudentNum = 29480
random.seed(myStudentNum)
np.random.seed(myStudentNum)


'''
Data structures
state:          the current candidate solution
clauses:        list of lists, each list contains the literal of the clause
unsat_clauses:  the index of each currently unsat clause
makecounts:     the current makecount for each variable 
                (number of currently unsat clauses involving the variable) 
breakcounts:    the current breakcount for each variable 
                (number of currently sat clauses involving the variable, 
                 where the variable is the only satisfying literal of the clause
                 i.e the clause will go unsat if this variable is flipped) 
litToClauses:   dictionary containing 2*vars entries, one for each literal associated with each variable

NB: The variables and their associated literals are numbered 1..n rather than 0..n-1, 
so to allow us to index in with variable number without having to -1 every time, 
a lot of the data structures are set up to be of size n+1, with the first element 
(index 0) ignored
'''

class GSAT_solver:
    
    def __init__(self, file, _h, _wp, _maxFlips, _maxRestarts, _tl):
        self.maxFlips = _maxFlips   # input: Number of flips before restarting
        self.maxRestarts = _maxRestarts     # input: Number of restarts before exiting
        self.wp = _wp   # input: walk probability
        self.h = _h     # input: heuristic to choose variable
        self.tl = _tl   # input: tabu length
        self.flips = 0              # current number of flips performed
        self.badflips = 0              # current number of bad flips performed (flips where obj fn was worse after flipping)
        self.restarts = 0           # current number of restarts performed
        self.nVars, self.nClauses, self.clauses, self.litToClauses = -1,-1,[],{}
        self.readInstance(file)
        self.state = [0 for _ in range(self.nVars+1)] # State stores current state (i.e. current solution)
        self.makecounts = np.zeros(self.nVars+1,dtype=int) # unsat that would go sat
        self.breakcounts = np.zeros(self.nVars+1,dtype=int) # sat that would go unsat
        self.lastFlip = np.full(self.nVars+1,-self.tl) # Iteration that variable was last updated in
        self.lastFlip[0] = self.maxFlips
        self.bestSol = [0 for _ in range(self.nVars)]
        self.bestObj = self.nClauses+1          # Current best objective found so far (obj of bestSol)
        self.bestObjForRestart = self.nClauses+1
        self.breakcounts[0] = self.nClauses+1 # sat that would go unsat

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

    def flip(self, variable):
        self.flips += 1
        self.state[variable] *= -1
        self.update_counts(variable)
        self.lastFlip[variable] = self.flips

    # Function to update objective value and counts of variables 
    # Run after flipping 
    def update_counts(self, variable):
        literal = self.state[variable]
        for clauseInd in self.litToClauses[literal]:
            satLits = 0
            if clauseInd in self.unsat_clauses:
                for lit in self.clauses[clauseInd]:
                    self.makecounts[abs(lit)] -= 1
                # Was unsat so only flipvar now satisfies it 
                self.breakcounts[variable] += 1
            else:
                for lit in self.clauses[clauseInd]:
                    if lit in self.state:
                        satLits += 1
                        if lit != literal:
                            breaklit = lit
                if satLits == 2:
                    self.breakcounts[abs(breaklit)] -=1
        self.unsat_clauses = self.unsat_clauses - self.litToClauses[literal]
        for clauseInd in self.litToClauses[literal*(-1)]:
            satLits = 0
            cStatus = False
            for lit in self.clauses[clauseInd]:
                if lit in self.state:
                    cStatus = True
                    satLits += 1
                    breaklit = lit
            if satLits == 1:
                self.breakcounts[abs(breaklit)] += 1
            if not cStatus:
                self.breakcounts[variable] -= 1 # flipvar was only 1 satisfying it
                self.unsat_clauses.add(clauseInd)
                for lit in self.clauses[clauseInd]:
                    self.makecounts[abs(lit)] += 1
        self.obj = len(self.unsat_clauses)

    def selectVar(self):
        if self.h =="gsat":
            return self.selectGSATvar()
        elif self.h == "gwsat":
            return self.selectGWSATvar()
        elif self.h == "hsat":
            return self.selectHSATvar()
        elif self.h == "walksat":
            return self.selectWalkSATvar()
        elif self.h == "hsatTabu":
            return self.selectHSATtabuvar()
        elif self.h == "grimesHsat":
            return self.selectGrimesHSATvar()
        else:
            return self.selectGrimesWSATvar()

        
    def selectGSATvar(self):
        gains = self.makecounts-self.breakcounts
        hvars = np.where( gains == np.amax(gains))[0]
        return np.random.choice(hvars)
        
    def selectRWvar(self):
        hvars = np.where( self.makecounts > 0 )[0]
        return np.random.choice(hvars)

    def selectGWSATvar(self):
        if random.random() < self.wp:
            nextvar = self.selectRWvar()
        else:
            nextvar = self.selectGSATvar()
        return nextvar

    def selectHSATvar(self):
        gains = self.makecounts-self.breakcounts
        hvars = np.where( gains == np.amax(gains))[0]
        return hvars[np.where(self.lastFlip[hvars]== np.amin(self.lastFlip[hvars]))[0]][0]

    def selectWalkSATvar(self):
        nextCls = random.choice(tuple(self.unsat_clauses))
        varsCls = [abs(lit) for lit in self.clauses[nextCls]]
        gains = np.array([self.breakcounts[i] for i in varsCls])
        hvars = np.where( gains == 0)[0]
        if len(hvars)>0:
            return varsCls[np.random.choice(hvars)]
        elif random.random() < self.wp:
            return random.choice(varsCls)
        else:
            hvars = np.where( gains == np.amin(gains))[0]
            return varsCls[np.random.choice(hvars)]

    def selectHSATtabuvar(self):
        '''
        Add tabu search to basic hsat, with aspiration criteria of 
        improving on best solution found so far in this search attempt 
        (i.e. not including from previous restarts).
        Advice: adapt Hsat code from selectHSATvar and add
        tabu criteria using LastFlip data structure
        '''
        gains = self.makecounts - self.breakcounts
        hvars = np.where(gains == np.amax(gains))[0]

        # Aspiration criteria: Allow tabu move only if it improves on best solution
        best_gain = np.amax(gains)
        if self.obj - best_gain < self.bestObjForRestart:
            return np.random.choice(hvars)

        # Variable is tabu if lastFlip + tabu length >= current iteration
        non_tabu_filter = self.lastFlip[hvars] + self.tl < self.flips
        non_tabu = hvars[non_tabu_filter]

        # If non-tabu variables exist, select maximum age variable of non tabu variables
        if len(non_tabu) > 0:
            return non_tabu[np.where(self.lastFlip[non_tabu] == np.amin(self.lastFlip[non_tabu]))[0]][0]

        # No improvement possible, select maximum age variable
        return hvars[np.where(self.lastFlip[hvars] == np.amin(self.lastFlip[hvars]))[0]][0]

    def selectGrimesWSATvar(self):
        '''
        (a) If zero damage variable, zero damage variable step 
            (select maximum positive gain variable from variables with positive gain > 0, 
             and negative gain = 0, if such variables exists)
        (b) Random walk step with probability wp:
                choose randomly from variables involved in at least one unsatisfied clause
        (c) Otherwise randomly choose unsat clause and choose variable with maximum net gain, breaking ties randomly
        Advice: adapt WalkSAT code from selectWalkSATvar
        '''
        # Positive gain is the number of variables that are unsat that will go sat
        # negatice gain is the number of variables that are sat that will go unsat
        # next gain is the sum of unsat  - the sum of unsat when we flip a variable.
        zero_damage_variables = self._get_zero_damage_variables()
        if len(zero_damage_variables) > 0:
            return np.random.choice(zero_damage_variables)

        random_unsat_clause = self._select_random_unsat_clause()

        if random.random() < self.wp:
            # TODO: is this all clauses? it says at least one.
            unsat_variables = self._get_all_variables_in_unsat_clauses()
            return np.random.choice(unsat_variables)

        return self._select_max_gain_variable_from_clause(random_unsat_clause)

    def selectGrimesHSATvar(self):
        '''
        (a) If zero damage variable, zero damage variable step 
            (select maximum positive gain variable from variables with positive gain > 0, 
             and negative gain = 0, if such variables exists)
        (b) Age walk step with probability wp:
                choose variable involved in at least one unsatisfied clause that was flipped the least recently
        (c) Otherwise randomly choose unsat clause and choose variable with maximum net gain, breaking ties randomly
        Advice: adapt WalkSAT code from selectWalkSATvar
        '''
        zero_damage_variables = self._get_zero_damage_variables()
        if len(zero_damage_variables) > 0:
            return np.random.choice(zero_damage_variables)

        if random.random() < self.wp:
            unsat_variables = self._get_all_variables_in_unsat_clauses()
            return unsat_variables[np.where(self.lastFlip[unsat_variables] == np.amin(self.lastFlip[unsat_variables]))[0]][0]

        random_unsat_clause = self._select_random_unsat_clause()
        return self._select_max_gain_variable_from_clause(random_unsat_clause)

    def _get_all_variables_in_unsat_clauses(self):
        """Returns all variables involved in all unsatisfied clause."""
        variables = set()
        for clause_index in self.unsat_clauses:
            for literal in self.clauses[clause_index]:
                variables.add(abs(literal))
        return np.array(list(variables))

    def _select_random_unsat_clause(self):
        """Select a random unsatisfied clause."""
        return random.choice(tuple(self.unsat_clauses))

    def _select_max_gain_variable_from_clause(self, clause_index):
        """
        Select a variable with maximum net gain from a clause.
        Break ties randomly.
        """
        variables = self._get_variables_from_clause(clause_index)
        net_gains = self._calculate_gains(variables)
        gains = self._get_gains_array(net_gains)
        return variables[np.random.choice(gains)]

    def _get_variables_from_clause(self, clause_index):
        """Get variables from a clause"""
        return [abs(lit) for lit in self.clauses[clause_index]]

    def _calculate_gains(self, variables):
        """Calculates gain """
        return np.array([self.makecounts[var] - self.breakcounts[var] for var in variables])

    def _get_gains_array(self, gains):
        """Returns an array of indices of maximum gain."""
        return np.where(gains == np.amax(gains))[0]

    def _get_zero_damage_variables(self):
        """Returns variables with positive gain and zero damage."""
        return np.where((self.makecounts > 0) & (self.breakcounts == 0))[0]
        
    def solve(self):
        self.restarts = 0
        totalFlips = 0
        while self.restarts < self.maxRestarts and self.bestObj > 0:
            self.bestObjForRestart = self.nClauses+1
            self.restarts += 1
            self.generateSolution()
            self.initial_cost()
            self.flips = 0
            self.lastFlip = np.full(self.nVars+1,-self.tl)
            self.lastFlip[0] = self.maxFlips
            while self.flips < self.maxFlips and self.bestObj > 0:
                nextvar = self.selectVar()
                self.flip(nextvar)
                if self.obj < self.bestObjForRestart:
                    self.bestObjForRestart = self.obj
                if self.obj < self.bestObj:
                    self.bestObj = self.obj
                    self.bestSol = self.state[1:]
            totalFlips += self.flips

        if self.bestObj == 0:
            solutionChecker(self.clauses, self.bestSol)
        return totalFlips, self.restarts, self.bestObj

def solutionChecker(clauses, sol):
    unsat_clause = 0
    for clause in clauses:
        cStatus = False
        for var in clause:
            if var in sol:
                cStatus = True
                break
        if not cStatus:
            unsat_clause+=1
    if unsat_clause > 0:
        print ("UNSAT Clauses: ",unsat_clause)
        return False
    return True



def main():
    if len(sys.argv) == 1: 
        filesDir = "uf150-645" 
        alg, nRuns, maxRes, maxFlips, wp, tl = "gwsat", 10, 50, 500, 0.1, 10
    elif len(sys.argv) < 8:
        print(len(sys.argv))
        print ("Error - Incorrect input")
        print ("Expecting python gsat.py [fileDir] [alg] [number of runs] [max restarts]",
               "[max flips] [walk prob]")
        sys.exit(0)
    else:
        _, filesDir, alg, nRuns, maxRes, maxFlips, wp, tl  = sys.argv
        nRuns, maxRes, maxFlips, wp, tl = int(nRuns), int(maxRes), int(maxFlips), float(wp), int(tl)
    

    # Iterate through all instances in the directory that end with 
    # last value of your student number 
    statsList = ["Inst", "Solved:", "Obj:","Res:", "Flips:","Time:"]
    format_row = "{:>12}"*(len(statsList)) 
    print(alg, nRuns, maxRes, maxFlips, wp)
    print(format_row.format(*statsList))
    for filename in listdir(filesDir):
        if filename.endswith(str(myStudentNum)[-1]+".cnf"):
            satInst=filesDir+"/"+filename
            avgRestarts, avgFlips, avgUnsatC, avgTime, unsolved = 0, 0, 0, 0, 0

            for i in range(nRuns):
                random.seed(myStudentNum + i*100)
                np.random.seed(myStudentNum + i*100)
                gsat = GSAT_solver(satInst, alg, wp, maxFlips, maxRes, tl)
                startPython = perf_counter()
                ctrFlips, ctrRestarts, ctrObj = gsat.solve()
                stopPython = perf_counter()
                avgFlips += ctrFlips
                avgRestarts += ctrRestarts
                avgUnsatC += ctrObj
                avgTime += (stopPython-startPython)
                if ctrObj > 0:
                    unsolved += 1
            resList = [filename, nRuns - unsolved, avgUnsatC/nRuns, avgRestarts/nRuns, avgFlips/nRuns, round(avgTime/nRuns,3)]
            print(format_row.format(*resList))

'''
Reading in parameters, but it is up to you to implement what needs implementing
TO DO:
1/ Update "myStudentNum" variable to your student number (line 14 in this file)
2/ Implement HsatTabu, grimesWsat, grimesHsat
3/ Implement alternative stopping condition involving badFlips
'''
            
main()
