
# coding: utf-8

# This code executes the following steps:
# 1) Set up district health service delivery cost estimate data
# 2) Calculate proportional allocation based on total cost of Essential Health Package (EHP) delivery
# 3) Merge with % of cost borne by partner by disease programme
# 4) Calculate proportional allocation based on government's share of cost of Essential Health Package (EHP) delivery
# 5) Run simulations on convergence to targeted allocation of resources assuming that no district suffers a reduction in its absolute budget size, even as proportional allocation reduces

# In[467]:


import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import squarify

plt.style.use('ggplot')


# In[468]:


## Set up Essential Health Package (EHP) cost data

raf_raw = pd.read_csv("raf_malawi_v2.csv",sep=',',header=0)
raf_final =raf_raw.rename({'District':'district', 
                    'Total RMNCH cost':'rmnch',
                    'Total Vaccine cost':'epi', 
                    'Total Malaria cost':'malaria',
                    'Total Nutrition cost':'nutrition',
                    'Total HIV/AIDS cost':'hiv',
                    'Total NCDs cost':'ncd',
                    'Total TB cost':'tb',
                    'Total Mental Health cost':'mental',
                    'Total IMCI cost':'imci',
                    'Total Oral Health cost':'oral',
                    'Current Allocation':'current_alloc'},axis=1)

raf_final = raf_final[0:32][:] # drop total row from dataframe
raf_final['fullcost'] = raf_final[ehp_prog].sum(axis=1) # Add Total EHP cost column
#raf_final.head()


# In[469]:


# Store EHP program names in a list

ehp_prog = list(raf_final.columns[1:11].values)


# In[470]:


# Calculate proportional allocation to district based on total cost of EHP delivery

raf_final['targ_alloc_fullcost'] = raf_final['fullcost']/(raf_final['fullcost'].sum(axis=0))


# In[471]:


## Set up data on partner contribution to EHP programs

partner_share = pd.read_csv("partner_share.csv",sep=',',header=0)
partner_share = partner_share.drop(columns = ['Unnamed: 0'])
partner_share=partner_share.rename({'% of RMNCH budget funded by partners':'rmnch',
                    '% of Vaccine budget funded by partners':'epi', 
                    '% of Malaria budget funded by partners':'malaria',
                    '% of Nutrition budget funded by partners':'nutrition',
                    '% of HIV/AIDS budget funded by partners':'hiv',
                    '% of NCDs budget funded by partners':'ncd',
                    '% of TB budget funded by partners':'tb',
                    '% of Mental Health budget funded by partners':'mental',
                    '% of IMCI budget funded by partners':'imci',
                    '% of Oral Health budget funded by partners':'oral'},axis=1)
partner_share.rename(index={0:'commodities',1:'program'}, inplace=True)

for i in ehp_prog: #convert % values to numeric values
    partner_share[i] = partner_share[i].apply(lambda x: np.nan if x in ['-'] 
                                                                    else x[:-1]).astype(float)/100
    
partner_share_prog = partner_share[1:][:] # preserve partner share in total program costs

partner_share_long = partner_share_prog.T # transpose 
#partner_share.head()


# In[472]:


# Reshape EHP Cost data
raf_final_long = raf_final.set_index(['district']) # set district as index
raf_final_long = raf_final_long.stack(dropna=False) # reshape wide to long
raf_final_long = raf_final_long.reset_index()
raf_final_long = raf_final_long.rename({'level_1':'ehp_prog'},axis=1)
raf_final_long = raf_final_long.set_index(['ehp_prog'])
#raf_final_long.head()


# In[473]:


# Merge EHP Cost data with partner contribution data
raf_merged = raf_final_long.join(partner_share_long, how='outer')
raf_merged = raf_merged.drop(['fullcost','current_alloc','targ_alloc_fullcost'],axis=0)
raf_merged = raf_merged.rename({0:'cost',
                                'program':'partner_share%'},axis=1)
#raf_merged.head()


# In[474]:


# Calculate government's share in the cost of EHP delivery
raf_merged['govt_cost'] = (1 - raf_merged['partner_share%'])*raf_merged['cost']
raf_merged = raf_merged.reset_index()

raf_final2=raf_merged.pivot(index='district', columns='index', values=['cost','govt_cost']) # reshape long to wide
#raf_final2.head()


# In[475]:


# Calculate proportional allocation to district based on government share in the cost of EHP delivery
raf_govtcost = raf_final2.govt_cost
raf_govtcost = raf_govtcost.reset_index() 

raf_govtcost['fullcost'] = raf_govtcost[ehp_prog].sum(axis=1)
raf_govtcost['targ_alloc_govtcost'] = raf_govtcost['fullcost']/(raf_govtcost['fullcost'].sum(axis=0))
#raf_govtcost.head()


# In[476]:


# Merge the Total EHP cost data with government share in cost data
raf_final2 = pd.merge(raf_govtcost, raf_final , on='district')
#raf_final2.head()


# In[477]:


# Store current allocation in a list
D_init = raf_final2[['current_alloc']]
D_init = [i[0] for i in D_init.values.tolist()]


# In[478]:


# Store Full EHP Cost allocation in a list
D_targfullcost = raf_final2[['targ_alloc_fullcost']]
D_targfullcost = [i[0] for i in D_targfullcost.values.tolist()]


# In[479]:


# Store Government EHP Cost allocation in a list
D_targgovtcost = raf_final2[['targ_alloc_govtcost']]
D_targgovtcost = [i[0] for i in D_targgovtcost.values.tolist()]


# In[480]:


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

    #print(distribution)


# In[486]:


# Run sample simulation and 

D_targ = D_targfullcost
budget_yr1 = 22678619270
growth_rate = 0.15
sim_yrs = 30
paceofchange(sim_yrs, D_init,D_targ,budget_yr1,growth_rate)


# In[487]:


# Some useful visualizations
totalcost_malawi = raf_govtcost.sum(axis=0)
squarify.plot(sizes=totalcost_malawi.iloc[1:10],label = ehp_prog, alpha=.8) # weight of each disease - full EHP cost


# In[488]:


govtcost_malawi = raf_final.sum(axis=0)
squarify.plot(sizes=govtcost_malawi.iloc[1:10],label = ehp_prog, alpha=.8) # weight of each disease - government EHP cost

