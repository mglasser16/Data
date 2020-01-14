import pandas as pd
import numpy as np
import io
import matplotlib.pyplot as plt
import os

#Reference https://www.fuelcellstore.com/avcarb-mgl190

carb_area=(9**2)*np.pi #in mm^2
carb_v =  carb_area*0.19 #in mm^3
carb_den = 0.44*.001 #in/mm^3
carb_m=carb_v*carb_den

def graph(file):
    D = pd.read_table(file, sep='deliminator', engine='python', header=None)
    D.dropna(inplace = True)
    D = D[0].str.split("\t", expand = True)

    d_row = list(D[1]).index('0') #This means we cut the data when the time is zero.  To look at full data, use d_row = list(D[0]).index('#') + 1
    D = D.iloc[d_row : ,]

    D[1] = D[1].astype(float)
    D[2] = D[2].astype(float)
    D[3] = D[3].astype(float)
    


    D['capacity'] = D[1] * abs(D[3])/carb_m
    title = file.split("Data/")
    title2 = title[1]
    
    for cell in D[2]:
        if cell > D.iloc[0,2]:
            row = list(D[2]).index(cell)
            newc=D.iloc[row:,2]
            D['adjust']=newc
            D['adjust']=D['adjust'].shift(-1*row)
            break
   
    D[2] =D[2].where(D[2]<=D.iloc[0,2]) 
    print(D[2])
            
    if D.iloc[1,2] < 0:
        D['absolute'] = D[2]*-1
        plt.figure(3)
        plt.scatter(D[1], D['absolute'], marker='o', label = title2)
        plt.legend(framealpha=1, frameon=True);
        plt.xlabel('time (s)', fontsize=12)
        plt.ylabel('voltage (V)', fontsize=12)
    else:
        plt.figure(3)
        plt.scatter(D[1], D[2], marker='o', label = title2)
        plt.scatter(D[1], D['adjust'], marker='o', label = title2)
        plt.legend(framealpha=1, frameon=True);
        plt.xlabel('time (s)', fontsize=12)
        plt.ylabel('voltage (V)', fontsize=12)
        
    plt.figure(0)
    plt.scatter(D['capacity'], D[2], marker='o', label = title2)
    plt.xlabel('Capacity (A/g)', fontsize=12)
    plt.ylabel('voltage (V)', fontsize=12)
    plt.legend(framealpha=1, frameon=True);
#    plt.figure(1)
#    plt.scatter(D[1], D[3], marker='o')
#    plt.xlabel('time (s)', fontsize=12)
#    plt.ylabel('current (A)', fontsize=12)

path = 'C:/Users/Amy LeBar/Documents/Data'
for file in os.listdir('C:/Users/Amy LeBar/Documents/Data'):
    if file.find('20191213_c001') > -1:
        graph(path + "/"+ file)

