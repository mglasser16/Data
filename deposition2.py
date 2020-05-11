#%%

# Useful libraries
import math as m
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import pandas as pd

# User imput variables
time = 11 #s
timespan = [0,time]
sites = 100

#constants
MW = 45.881 #g/mol
den = 2.31 #g/cm³
V_den = MW/den

#nucleation
k_nuc = 20000 #reaction constant
a_nuc = 4.5 #activation energy
r0 =1
#growth
k_grow =3
n = 2 #reaction constant
c_k = 1.5#concentratiosn of precipitant
co_k = 1 #100% saturation
S = c_k/co_k
n_0 = 0 #possibly outdated
theta =float((sites- n_0)/sites) #possibly outdated

#iterative array in dictionary form
constants = {}
constants['r_0'] = 1
constants['n_0'] = 0
constants['theta'] = (sites-constants['n_0'])/sites
constants['S'] = c_k/co_k
rad =[]

#intializing constants
initial = {}
initial['r_0'] =1
initial['n_0'] =0
initial['theta_0'] = (sites- initial['n_0'])/sites
prop_0 = list(initial.values())

#for time graph
r = np.empty([0])
nuc = [constants['n_0']]
N_tot =[constants['n_0']]

#ODE solver sundials
#%%

def func(t,varbs_array):
    radius = varbs_array[0]
    drad_dt = V_den/2*radius*k_grow*(constants['S']-n)**n
    return [drad_dt]

sol = solve_ivp(func, timespan, prop_0)

radius = sol.y[0]
t = sol.t
plt.plot(t,radius)
#%%

def func2(t,varbs_array2):
    radius2, nucl2, theta2 = varbs_array2
    if theta2 > 0.0:
        drad_dt2 = V_den/2*radius2*k_grow*(constants['S']-n)**n
        dnucl_dt2 = k_nuc*theta2*m.exp(-a_nuc/(n*m.log(S)))
        dtheta_dt2 = -k_nuc*theta2*m.exp(-a_nuc/(n*m.log(S)))/sites
    else:
        drad_dt2 = V_den/2*radius2*k_grow*(constants['S']-n)**n
        dnucl_dt2 =0
        dtheta_dt2 =0
    return drad_dt2, dnucl_dt2, dtheta_dt2

sol2 = solve_ivp(func2, timespan, prop_0)

radius2 = sol2.y[0]
nucl2 = sol2.y[1]
theta2 = sol2.y[2]
time2 =sol2.t
print(theta2)
#%%
mass = []
print (mass)
for tim in range(len(time2)):
    mass[tim] = theta2[tim]
    print(mass)


# for t in np.arange(time/dt):
#     dr_dt =  V_den/2*constants['r_0']*k_grow*(constants['S']-n)**n
#     constants['r_0'] = constants['r_0']+dr_dt*dt
#     rad.append(constants['r_0'])
#     print(rad)

# dN_dt = 2
# for t in np.arange(time/dt):
#     #nucleation step
#     if dN_dt > 1:
#         dN_dt =k_nuc*theta*m.exp(-a_nuc/(n*m.log(S)))
#         nuc.append(dN_dt)
#         print ("dN_dt: ", dN_dt)
#         print ("r: ", r)
#         dtheta_dt = -dN_dt/sites
#         theta = theta + (dtheta_dt*dt)
#         r = np.append(r, r0)
#         dr_dt =  r*np.array(V_den/2*k_grow*(S-n)**n)
#         print ("dr_dt: ", dr_dt)
#         r = r+dr_dt*dt
#         print ("r2: ", r)
#     else:
#         dr_dt =  r*np.array(V_den/2*k_grow*(S-n)**n)
#         r = r+dr_dt*dt
#         print ("r2: ", r)






# %%
