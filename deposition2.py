#%%

# Useful libraries
import math as m
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import pandas as pd
#import cantera as ct Cantera %Cantera working units (m, kg, kmol, s, J, K, Pa)

# User imput variables
time = 200 #s  - input desired duration
sites = 100 #input how many sites you desired to model
n_0 = 0  #input how many nucleations are already present
c_k = 1.5#concentratiosn of precipitant - should be in kmol/m³
co_k = 1 #100% saturation - should be in kmol/m³

#add site size ?

#constants
MW = 45.881 #kg/kmol
den =2310 #kg/m³ 2.31 #g/cm³
mol_vol = MW/den #m³/kmol
timespan = [0,time]

#calculated
S = c_k/co_k  # should go to initializing constants later

#nucleation
k_nuc = 20000 #reaction constant  #in radu = nucl/m²/sec #in Horstmann = mol/m²sec
a_nuc = 4.5 #activation energy

#growth
k_grow =3 #mol/m²/s
n = 2 #reaction constant

#intializing constants
initial = {}
initial['r_0'] =1 #m
#initial['n_0'] =0 #nuclations
initial['theta_0'] = (sites- n_0)/sites #unitless
sol_vec = list(initial.values())  # solution vector

#growth case
#%%

def growth(t,varbs_array):
    radius = varbs_array[0] #indicates variable array because I forget
    drad_dt = mol_vol*k_grow*(S-n)**n
    return [drad_dt]

growth_sen = solve_ivp(growth, timespan, sol_vec) #growth senario

radius = growth_sen.y[0]
t = growth_sen.t
plt.plot(t,radius)

#nuc and growth
#%%

def nucleation(t,varbs_array2):
    radius2, theta2 = varbs_array2
    if theta2 > 0.0:
        drad_dt2 = mol_vol*k_grow*(S-n)**n #in m/s
#        dnucl_dt2 = k_nuc*theta2*m.exp(-a_nuc/(n*m.log(S)))
        dtheta_dt2 = -k_nuc*theta2*m.exp(-a_nuc/(n*m.log(S)))/sites
    else:
        drad_dt2 = mol_vol*k_grow*(S-n)**n
#        dnucl_dt2 =0
        dtheta_dt2 =0
    return drad_dt2, dtheta_dt2

nucl_sen = solve_ivp(nucleation, timespan, sol_vec)

radius2 = nucl_sen.y[0]
#nucl2 = nucl_sen.y[1]
theta2 = nucl_sen.y[1]
print(theta2)
nucl2 = k_nuc*theta2*m.exp(-a_nuc/(n*m.log(S)))
print(nucl2)
time2 =nucl_sen.t
#%%
mass = np.zeros(len(time2))
back_nuc = nucl2[::-1]
#%%

for tim in range(len(time2)):
    if tim == 0:
        continue
    else:
        mass [tim]= sum((m.pi*2/3*den*(radius2[0:tim]**3))*back_nuc[0:tim])
        print (mass)


    # mass[tim] = theta2[tim]
    # print(mass)


# %%
