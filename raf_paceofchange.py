
# import pandas and numpy
import pandas as pd
import numpy as np

# The following lists are sample distributions of the total national budget. The final code will pull data for the 
# real allocations to 29 districts in Malawi
D_init = [0.1, 0.1, 0.1, 0.2, 0.2, 0.3]  # initial distribution

D_targ = [0.2, 0.2, 0.2, 0.2, 0.1, 0.1]  # target distribution

N = len(D_init) # number of districts

M = 50  # number of years

B = [None] * M

B[0] =  1000000 # This needs to be edited with the actual national resource envelope

g = 0.10 # annual growth rate of total budget


for i in range(M-1):

    B[i+1]=B[i]*(1+g)


# Define distribution array

D = [[None]*N]*M  

D[0] = D_init


# Define allocation array

A = [[None]*N]*M


# Calculate allocation in starting year (Year 0)

A[0] = [D[0][j]*B[0] for j in range(N)]

# Temporary arrays for use during annual iterations:

desired_budget = [None] * N

desired_delta = [None] * N

actual_delta = [None] * N


###########################################

# Annual Iteration

############################################

for i in range(M-1): # loop through years

    

    previous_alloc = A[i]

    this_alloc = [None]*N


    for j in range(N):

        desired_budget[j] = D_targ[j]*B[i+1]  # desired allocation in year i+1

        desired_delta[j] = max(0, desired_budget[j] - A[i][j])

    for j in range(N):

        total_delta = B[i+1] - B[i]

        actual_delta[j] = total_delta*desired_delta[j]/sum(desired_delta)

        this_alloc[j] = round(previous_alloc[j] + actual_delta[j],0)

        

    A[i + 1] =  this_alloc

    D[i+1] = [round(A[i+1][j]/B[i+1],4) for j in range(N)]


############################################

# Print Results

############################################



print("Year by year distributions")

for i in range(M):

    print("year", i, " :", D[i])



print("Year by year allocations")

for i in range(M):

    print("year", i, " :", A[i])



    
############################################

# Calculate number of years required

############################################

R = [D_init[j]/D_targ[j] for j in range(N)]

Rmax = max(R)

import math

years_needed = math.log(Rmax)/math.log(1+g)

print("years needed = ", years_needed)

