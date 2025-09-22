#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 11:00:00 2024

@author: dgrimes
"""
import sys

def readInstance(fName):
    file        = open(fName, 'r')
    tVariables  = -1
    tClauses    = -1
    clause      = []
    variables   = []

    current_clause = []

    for line in file:
        data = line.split()

        if len(data) == 0:
            continue
        if data[0] == 'c':
            continue
        if data[0] == 'p':
            tVariables  = int(data[2])
            tClauses    = int(data[3])
            
            continue
        if data[0] == '%':
            break
        if tVariables == -1 or tClauses == -1:
            print ("Error, unexpected data")
            sys.exit(0)

        ##now data represents a clause
        for var_i in data:
            literal = int(var_i)
            if literal == 0:
                clause.append(current_clause)
                current_clause = []
                continue
            var = literal
            if var < 0:
                var = -var
            if var not in variables:
                variables.append(var)
            current_clause.append(literal)

    if tVariables != len(variables):
        print ("Unexpected number of variables in the problem")
        print ("Variables", tVariables, "len: ",len(variables))
        print (variables)
        sys.exit(0)
    if tClauses != len(clause):
        print ("Unexpected number of clauses in the problem")
        sys.exit(0)
    file.close()
    return [variables, clause]

def readSolution(fName):
    file = open(fName, 'r')
    my_vars = {}
    my_vars2 = []
    for line in file:
        data = line.split()

        #print data
        if len(data) == 0:
            continue
        if data[0] == 'c':
            continue
        if data[0] == 'v':
            del data[0]
        for literal in data:
            literal = int(literal)
            if literal == 0:
                break
            my_vars2.append(literal)
            var = literal
            if var < 0:
                my_vars[-var] = 0
            else:
                my_vars[var] = 1
    file.close()
    return my_vars, set(my_vars2)