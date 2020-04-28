# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 10:46:57 2020

@author: corey_zjfshge
"""

from pulp import *

import math

MonthBudg = 99999999 #Monthly Budget

SGICost = 9000 #9000 is discounted cost in Months 1 and 2

SunCost = 18750 #18750 is the discounted cost in Months 1 and 2

alpha = 10000

# Server Capacity
ServerCap = {'1_Std-Pentium-Server':30, '2_Enh-Pentium-Server':80, '3_SGI-Server':200, '4_Sun-Server':2000}

# Server Cost
ServerCost = {'1_Std-Pentium-Server':2500, '2_Enh-Pentium-Server':5000, '3_SGI-Server':SGICost, '4_Sun-Server':SunCost}

# Minimum Number of Servers for each type =0
MinServer = {'1_Std-Pentium-Server':0, '2_Enh-Pentium-Server':0, '3_SGI-Server':0, '4_Sun-Server':0}

Staff = 50 #The number in the department minus the carryover from the previous month

# The number of services needed of each type
ServerCt = list(sorted(ServerCap.keys()))

# Create model
prob = LpProblem("Case 1 Part A", LpMinimize)

# Variables
x = LpVariable.dicts('x', ServerCt, lowBound=0, cat=pulp.LpInteger)

# Objective
prob += sum(ServerCost[i]*x[i] for i in ServerCt)

# Constraint
prob += sum(ServerCap[i]*x[i] for i in ServerCt) >= Staff
prob += sum(ServerCost[i]*x[i] for i in ServerCt) <= MonthBudg
prob += sum(ServerCost[i]*x[i]*alpha for i in ServerCt) - sum(ServerCap[i]*x[i] for i in ServerCt)

# Quantity of each Server:
for i in ServerCt:
    prob += x[i] >= MinServer[i]


# Optimize
prob.solve()

prob.writeLP("Group 13: Case 1 Part A")
status = prob.solve()

print(prob)

prob.solve() 
print("Optimization Status: " + LpStatus[prob.status]) 
print('\n')
print('How many of each server to buy:')
for variable in prob.variables():
     print("{} = {}".format(variable.name, math.ceil(variable.varValue))) 
     
MonthlyCost = math.ceil(value(prob.objective)/alpha)
print('Server(s) Cost $', MonthlyCost)
