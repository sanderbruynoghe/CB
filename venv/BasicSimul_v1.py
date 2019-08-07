#BasicSimul_v1.py
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from SimulElem_v1 import *

'''Parameters on dashboard eventually'''
#Load
    #For now: load data defined in Load class
    #But has to be random, or according to a given input from the dashboard
        #E.g.: different factors to set en magnitude of peak loads
#System components
    #Battery Pack: for now: 1 RESU10H LG Chem battery (see datasheet)
number_of_bat = 1
max_energy_one =
'''Initialize model'''
    #Consumer (house load)
load = Load()
    #Components
batterypack = BatteryPack(1, 9.3, 1, 5, 5) #1 RESU10H battery with 5kWh initially stored
fte = FuelTankElectrolyzer(100, 1, 0.5, 0.5, 5, 5, 50) # Random values for now
pvarray = PVArray(30, 330) #30 panels of 330 Wp power
grid = Grid()

    #Arrays for storing battery, fte and grid energy and power levels
bat_soc = []
bat_power_level = [] #Negative when charging?
fte_soc = []
fte_power_level = [] #Negative when charging?
    #Grid has no energy level
grid_power_level = [] #Negative when delivering to grid?



'''Discrete event simulation (can be executed inside a MonteCarlo Simulation with random consumption)'''
    #Test just for first date
for time in range(0,96):
    load_power = load.power[time]
    load_energy = load.energy[time]
#def update_model():
    #Load bigger than PV production: discharge battery and/or fte
    if load_power >= pvarray.power[time]:
        rest_power = load_power - pvarray.power[time]
        rest_energy = rest_power/4
        #Battery update
        if batterypack.soc > batterypack.min: #Battery can be used because energy left
            #The max power to deliver in the next 15 min is the min of the resting power, the maximum discharge power and the power to discharge to the min in the next 15 min
            batterypack.power = min(rest_power, batterypack.max_discharge, (batterypack.soc - batterypack.min)*4) #Power level for next 15 min
        else:
            batterypack.power = 0
        batterypack.discharge(batterypack.power / 4)  # Energy level will decrease with this value
        rest_power -= batterypack.power
        rest_energy -= batterypack.power / 4
        #FTE update
        if (rest_power > 0 and fte.soc > fte.min): #Battery not enough (rest_power > 0, and fte can be used because still energy
            fte.power = min(rest_power, fte.max_discharge, (fte.soc - fte.min)*4)
        else:
            fte.power = 0
        fte.discharge(fte.power / 4)
        rest_power -= fte.power
        rest_energy -= fte.power / 4
        #Grid update
        if rest_power > 0: #Still power needed --> grid supplies the rest
            grid.power = rest_power #Grid supplies everything else
            grid.prod += grid.power/4 #Total produced by grid increases
        else:
            grid.power = 0
    #Load smaller than PV production: charge battery and/or fte
    else:
        excess_power = pvarray.power[time] - load_power
        excess_energy = excess_power/4
        #Battery update
        if batterypack.soc < batterypack.cap: #Battery can be charged because not full
            batterypack.power = - min(excess_power, batterypack.max_charge, (batterypack.cap - batterypack.soc) *4 )
            #STILL CONFUSING WITH + AND -
        else:
            batterypack.power = 0
        batterypack.charge(-batterypack.power / 4)  # Energy level will decrease with this value
        excess_power += batterypack.power
        excess_energy += batterypack.power / 4
        #FTE update
        if (excess_power > 0 and fte.soc < fte.cap):  # Battery not enough (rest_power > 0, and fte can be used because still energy
            fte.power = - min(excess_power, fte.max_charge, (fte.cap - fte.soc) * 4)
        else:
            fte.power = 0
        fte.charge(- fte.power / 4)
        excess_power += fte.power
        excess_energy += fte.power / 4
        #Grid update
        if excess_power > 0:  # Still power needed --> grid supplies the rest
            grid.power = - excess_power  # Grid supplies everything else
            grid.cons -= grid.power / 4  # Total produced by grid increases
        else:
            grid.power = 0

    #Update variables for plots
    bat_power_level.append(batterypack.power)
    bat_soc.append(batterypack.soc)
    fte_power_level.append(fte.power)
    fte_soc.append(fte.soc)
    grid_power_level.append(grid.power)
print(bat_power_level)
'''Plotting outcome'''
plt.subplot(2,2,1)
plt.plot(bat_power_level)
plt.title('Battery Power Level')
plt.subplot(2,2,2)
plt.plot(bat_soc)
plt.title('Battery SOC')
plt.subplot(2,2,3)
plt.plot(fte_power_level)
plt.title('FTE Power Level')
plt.subplot(2,2,4)
plt.plot(fte_soc)
plt.title('FTE SOC')
plt.show()

plt.plot(grid_power_level)
plt.title('Grid Power delivery')
plt.show()
