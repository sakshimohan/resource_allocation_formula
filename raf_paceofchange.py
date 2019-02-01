
# import pandas and numpy
import pandas as pd
import numpy as np

M = 50  # number of years

# The following lists are sample distributions of the total budget for the purpose of perfecting the code
D_init = [0.1, 0.1, 0.1, 0.2, 0.2, 0.3]  # initial distribution

D_targ = [0.2, 0.2, 0.2, 0.2, 0.1, 0.1]  # target distribution

N= len(D_init) # number of districts

B = [None] * M

B[0] =  1000000

g = 0.10 # annular growth rate in total budget


for i in range(M-1):

    B[i+1]=B[i]*(1+g)


# Define distribution array

D = [[None]*N]*M  #(Creates a list of lists with empty entries)

D[0] = D_init


# Define allocation array

A = [[None]*N]*M


# Calculate allocation in starting year (Year 0)

A[0] = [D[0][j]*B[0] for j in range(N)]

# temporary arrays for use during annula iterations:


desired_budget = [None] * N

desired_delta = [None] * N

actual_delta = [None] * N


###########################################

# apply annual iteration strategy    

############################################

for i in range(M-1): #(loop through years)

    

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



########################################

R = [D_init[j]/D_targ[j] for j in range(N)]

Rmax = max(R)

import math

Years_needed = math.log(Rmax)/math.log(1+g)

print("years needed = ", Years_needed)

