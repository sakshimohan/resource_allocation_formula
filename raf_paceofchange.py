
# coding: utf-8

# In[175]:


# import pandas
import pandas as pd
import numpy as np


# In[176]:


# . raf_final = pd.read_csv("/Users⁩/sakshimohan/⁩Dropbox (Personal)/MOH Malawi⁩/Resource Allocation Formula⁩/Pace of Change/formula_allocations.csv",sep=',',header=1)

raf_final = pd.read_csv("formula_allocations.csv",sep=',',header=0)


# In[177]:


raf_final.head()


# In[178]:


M = 50  # number of years

#D_init = [0.1, 0.1, 0.1, 0.2, 0.2, 0.3]  # initial distribution

#D_targ = [0.2, 0.2, 0.2, 0.2, 0.1, 0.1]  # target distribution

D_init = raf_final[['Current allocation (amended)']]
D_init.head()


# In[179]:


D_init = [i[0] for i in D_init.values.tolist()]
print(D_init)


# In[180]:


# failed attempts

#D_targ = raf_final[['EHP intervention need allocation (full coverage)']]
#D_targ = np.transpose(D_targ)
#D_targ = np.array(D_targ).tolist()
#D_targ = np.transpose(D_targ)
#D_targ = np.hstack(D_targ)
#D_targ = np.concatenate([np.array(i) for i in D_targ])


# In[181]:


D_targ = raf_final[['EHP intervention need allocation (full coverage)']]
D_targ = [i[0] for i in D_targ.values.tolist()]
print(D_targ)


# In[182]:


N = len(D_init) # number of districts
N


# In[183]:


B = [None] * M

B[0] =  1000000

g = 0.15 # annular growth rate in total budget


# In[184]:


# Calculate Total annual budget for each year

for i in range(M-1):

    B[i+1]=B[i]*(1+g)


# In[185]:


# Define distribution array

D = [[None]*N]*M  #(Creates a list of lists with empty entries)

D[0] = D_init



# Define allocation array

A = [[None]*N]*M


# In[186]:


# Calculate allocation in starting year (Year 0)

A[0] = [D[0][j]*B[0] for j in range(N)]

# temporary arrays for use during annula iterations:



desired_budget = [None] * N

desired_delta = [None] * N

actual_delta = [None] * N


# In[187]:


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


# In[190]:


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


# In[191]:


R = [D_init[j]/D_targ[j] for j in range(N)]

Rmax = max(R)

import math

Years_needed = math.log(Rmax)/math.log(1+g)

print("years needed = ", Years_needed)

