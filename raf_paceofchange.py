
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


for year in range(M-1):

    B[year+1]=B[year]*(1+g)


# Define distribution array

D = [[None]*N]*M  

D[0] = D_init


# Define allocation array

A = [[None]*N]*M


# Calculate allocation in first year

A[0] = [D[0][district]*B[0] for district in range(N)]

# Temporary arrays for use during annual iterations:

desired_budget = [None] * N

desired_delta = [None] * N

actual_delta = [None] * N


###########################################

# Annual Iteration

############################################

for year in range(M-1): # loop through years

    

    previous_alloc = A[year]

    this_alloc = [None]*N


    for district in range(N):

        desired_budget[district] = D_targ[district]*B[year+1]  # desired allocation in year i+1

        desired_delta[district] = max(0, desired_budget[district] - A[year][district])

    for district in range(N):

        total_delta = B[year+1] - B[year]

        actual_delta[district] = total_delta*desired_delta[district]/sum(desired_delta)

        this_alloc[district] = round(previous_alloc[district] + actual_delta[district],0)

        

    A[year + 1] =  this_alloc

    D[year+1] = [round(A[year+1][district]/B[year+1],4) for district in range(N)]


############################################

# Print Results

############################################



print("Year by year distributions")

for year in range(M):

    print("year", year, " :", D[year])



print("Year by year allocations")

for year in range(M):

    print("year", year, " :", A[year])



    
############################################

# Calculate number of years required

############################################

R = [D_init[district]/D_targ[district] for district  in range(N)]

Rmax = max(R)

import math

years_needed = math.log(Rmax)/math.log(1+g)

print("years needed = ", years_needed)

