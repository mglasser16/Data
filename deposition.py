#%%
# Useful libraries
import math as m
import numpy as np
import random as r

# Imput variables

time = 1 #hrs
dt= 0.5 #hrs

#Constants for nucleation
k_nuc = 9000 #reaction constant
theta = 1 # fraction of nucleation sites
a_nuc = 4.5 #activation energy
n = 2 #reaction constant
c_k = 1.5#concentration of precipitant
co_k = 1 #100% saturation
nx = 12

#Constants for growth
k_grow = 9

#Calculated variables
S = c_k/co_k
# Rough Calculation of rates
S_nuc_1 = np.around(k_nuc*theta*m.exp(-a_nuc/(n*m.log(S))),0)
S_grow = k_grow*(S-n)**n #in kmole/m^2/s order *E-6

# populate rows of an array
nucl_mol = list(np.zeros(nx))
nucl_start = 1E-8 #order of E-7 mol/liter/min

#conversion
MW = 45.881 #g/mol
den = 2.31 #g/cm³
for t in np.arange(time/dt):
    print (t)
    print(nucl_mol)
    count = 0
    theta=nucl_mol.count(0)/nx
    S_nuc_1 = np.around(k_nuc*theta*m.exp(-a_nuc/(n*m.log(S))),0)
    while count < S_nuc_1:
        if nucl_mol.count(0)==0:
            break
        for i in range(len(nucl_mol)):
            if nucl_mol[i] ==0:
                count = count + 1
                if r.randint(1,10)*.1 <.5:
                    nucl_mol[i] = nucl_start
                    if nucl_mol.count(0)==0:
                        continue
    for i in range(len(nucl_mol)):
        if nucl_mol[i] != 0:
            V = nucl_mol[i]*MW*den
            Rad= (3/2*V/np.pi)**(1/3)
            nuc_area = 2*np.pi*Rad**2
            nucl_mol[i] = nucl_mol[i] + S_grow*nuc_area*dt






# %%
