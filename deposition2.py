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
c_k = 1.5 #concentratiosn of precipitant - should be in kmol/m³
co_k = 1 #100% saturation - should be in kmol/m³
V_elect = 10*initial['r_0']
#add site size ?

#constants
R = 8314.4 #J/K / kmol
T = 298 #K
surf_energy = 0.54 #J / m² temp data for lithium... (http://crystalium.materialsvirtuallab.org/)
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
initial['r_0'] = 2**surf_energy*(1/mol_vol)/(R*T*m.log(S)) #m
#initial['n_0'] =0 #nuclations
initial['theta_0'] = (sites- n_0)/sites #unitless
initial['S'] = c_k/co_k #unitless
sol_vec = list(initial.values())  # solution vector
print(sol_vec)

#will vary at some point?
A_spec = (10*initial['r_0'])**2/(V_elect)**3 #Specific surface of reaction (m²/m³) using r_0 for scale
int_volume =  2/3*initial['r_0']**3

#growth case
#%%

def growth(t,varbs_array):
    radius = varbs_array[0] #indicates variable array because I forget
    drad_dt = mol_vol*k_grow*(S-1)**n
    return [drad_dt]

growth_sen = solve_ivp(growth, timespan, sol_vec) #growth senario

radius = growth_sen.y[0]
t = growth_sen.t
plt.plot(t,radius)

#nuc and growth
#%%

def nucleation(t,varbs_array2):
    radius2, theta2, conc = varbs_array2
    # if theta2 > 0.0:
    drad_dt2 = mol_vol*k_grow*(conc-1)**n#in m/s
#        dnucl_dt2 = k_nuc*theta2*m.exp(-a_nuc/(n*m.log(S)))
    dtheta_dt2 = -k_nuc*theta2*m.exp(-a_nuc/(n*m.log(conc)))/sites
#     else:
#         drad_dt2 = mol_vol*k_grow*(S-1)**n
# #        dnucl_dt2 =0
#         dtheta_dt2 =0
    dconc_dt = A_spec*dtheta_dt2*sites*int_volume/mol_vol #-drad_dt2*2*m.pi*radius2**2 doesn't work unsure
    return drad_dt2, dtheta_dt2, dconc_dt

nucl_sen = solve_ivp(nucleation, timespan, sol_vec)

radius2 = nucl_sen.y[0]
#nucl2 = nucl_sen.y[1]
theta2 = nucl_sen.y[1]
concen = nucl_sen.y[2]

t2 = nucl_sen.t
print(theta2)
print(radius2)
print(concen)
nucl2 = k_nuc*theta2*m.exp(-a_nuc/(n*m.log(S)))

plt.plot(t2, radius2)
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
