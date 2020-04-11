#%%

# Useful libraries
import math as m
import numpy as np

# Imput variables
time = 11 #s
dt= 1 #s
sites = 100

#constants
MW = 45.881 #g/mol
den = 2.31 #g/cm³
V_den = MW/den

#nucleation
k_nuc = 9000 #reaction constant
a_nuc = 4.5 #activation energy
r0 =1
#growth
k_grow =3
n = 2 #reaction constant
c_k = 1.5#concentratiosn of precipitant
co_k = 1 #100% saturation
S = c_k/co_k
n_0 = 0
theta =float((sites- n_0)/sites)



#iterative array in dictionary form
constants = {}
constants['r_0'] = 1
constants['n_0'] = 0
constants['theta'] = (sites-constants['n_0'])/sites
constants['S'] = c_k/co_k
rad =[]

#for time graph
r = np.empty([0])
nuc = [constants['n_0']]
N_tot =[constants['n_0']]

#ODE solver sundials

for t in np.arange(time/dt):
    dr_dt =  V_den/2*constants['r_0']*k_grow*(constants['S']-n)**n
    constants['r_0'] = constants['r_0']+dr_dt*dt
    rad.append(constants['r_0'])
    print(rad)

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
