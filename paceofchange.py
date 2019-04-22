## PACE OF CHANGE SIMULATION

# Define a function which simluates year-on-year change in proportional allocations to arrive at the target allocation

def paceofchange(sim_yrs, D_init,D_targ,budget_yr1,growth_rate):
    N = len(D_init)
    M = sim_yrs  # number of years

    B = [None] * M
    B[0] =  budget_yr1

    g = growth_rate
    
    # Calculate Total annual budget for each year

    for i in range(M-1):

        B[i+1]=B[i]*(1+g)
        
    # Define (empty) distribution array

    D = [[None]*N]*M  

    D[0] = D_init


    # Define (empty) allocation array

    A = [[None]*N]*M
    
    
    # Calculate allocation in starting year (Year 0)

    A[0] = [D[0][j]*B[0] for j in range(N)]

    # Define temporary arrays to be used in annual iterations:

    desired_budget = [None] * N

    desired_delta = [None] * N

    actual_delta = [None] * N
    
    # ANNUAL ITERATION

    for i in range(M-1): #(loop through years)



        previous_alloc = A[i]

        this_alloc = [None]*N


        for j in range(N): #(loop through districts)

            desired_budget[j] = D_targ[j]*B[i+1]  # desired allocation in year i+1

            desired_delta[j] = max(0, desired_budget[j] - A[i][j]) # no district budget should reduce in absolute terms

        for j in range(N):

            total_delta = B[i+1] - B[i] # budget increase

            actual_delta[j] = total_delta*desired_delta[j]/sum(desired_delta) # proportional distribution of budget increase 

            this_alloc[j] = round(previous_alloc[j] + actual_delta[j],0)



        A[i + 1] =  this_alloc

        D[i+1] = [round(A[i+1][j]/B[i+1],4) for j in range(N)]
        
    # Store results in a dataframe
    
    distribution = pd.DataFrame(D)
    distribution.columns = distribution.columns+1
    distribution.index = distribution.index + 1
    distribution = distribution.T
    distribution = distribution.reset_index()
    
    distname = raf_final2['district'] 
    distribution = distribution.join(distname, how='outer') # merge district names
    
    cols = list(distribution)
    cols.insert(0, cols.pop(cols.index('district'))) # move district column to the beginning
    distribution = distribution[cols]
    
    R = [D_init[j]/D_targ[j] for j in range(N)]

    Rmax = max(R)

    import math

    Years_needed = round(math.log(Rmax)/math.log(1+g),1)

    print("years needed to arrive at final allocation = ", Years_needed)
    
    distribution.to_csv("raf_distribution_simulation.csv",sep="\t") # Store results in .csv file
    
    print("Results stored in .csv file for Targeted distribution", D_targ)

    
# Run sample simulation and store results

D_targ = D_targfullcost
budget_yr1 = 22678619270
growth_rate = 0.10
sim_yrs = 30
paceofchange(sim_yrs, D_init,D_targ,budget_yr1,growth_rate)
