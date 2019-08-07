#BasicSimul_v2.py
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from SimulElem_v2 import *

'''Parameters on dashboard eventually'''
#Load: for now: just SLP from VREG with 13000 kWh year consumption
    #But has to be random, or according to a given input from the dashboard
        #E.g.: different factors to set en magnitude of peak loads
#System components
    #Battery Pack: for now: 3 RESU10H LG Chem battery (see datasheet)
number_of_batt = 3
usable_energy_one = 9.3     #Usable energy of single battery [kWh]
min_energy_one = 1          #Minimal soc level of battery (to avoid high voltage drop) [kWh]
max_charge_bat = 5          #Max charging power (single battery) [kW]
max_discharge_bat = 5       #Max discharging power (single battery) [kW]
init_soc_bat = 5            #Initial state of charge of each battery [kWh]
    #PV Array: for now: 30 panels of 330 Wp (future situation of house) and production according to Elia data
number_of_pv = 30           #Number of pv panels in array
Wp = 330                    #Peak Power of panels [kW]
    #FuelCell-Tank-Electrolyzer combination: for now: VERY STRONG ASSUMPTIONS AND SIMPLIFICATIONS
    #Based on Intelligent Energy FCM-802 & NEL proton PEM S40
max_soc = 1000              #Max energy stored in tank [kWh]
min_soc = 1                 #Min energy stored in tank [kWh]
fuel_cell_factor = 0.57     #Power conversion factor of Fuel Cell [-]
electr_factor = 0.57        #Power conversion factor of Electrolyzer [-]
                            #Combined: 0.57*0.57=0.33 efficiency
max_charge_fte = 5          #Max charging power [kW]
max_discharge_fte = 5       #Max discharging power [kW]
init_soc_fte = 800          #Initial state of charge [kWh]
    #Grid: for now: (dis)charging with infinite power
#Data time intervals
time_interval = 15*60                   #15*60 sec between each power measurement
conv_factor = time_interval/(60*60)     #x kW for time_interval sec: x*time_interval/(60*60) kWh energy used in interval

'''Initialize model'''
#Load (house)
load = Load()
#System Components
batterypack = BatteryPack(number_of_batt, usable_energy_one, min_energy_one,
                          max_charge_bat, max_discharge_bat, init_soc_bat)
pvarray = PVArray(number_of_pv, Wp)
fte = FuelTankElectrolyzer(max_soc, min_soc, fuel_cell_factor, electr_factor,
                           max_charge_fte, max_discharge_fte, init_soc_fte)
grid = Grid()

#Arrays for storing battery, fte and grid energy and power levels
    #Battery
bat_soc = []
bat_power_level = []
    #FTE
fte_soc = []
fte_power_level = []
    #Grid
grid_power_level = []
grid_prod_total = []
grid_cons_total = []


'''Discrete event simulation (can be executed inside a MonteCarlo Simulation with random consumption)'''
    #For now: test for 01/01/2018 only (first 96 data points)
        #01/01/2018 - 07/01/2018: (0,672)
        #01/07/2018 - 07/07/2018: (17372, 18043)
        #01/03/2018 - 31/10/2018: (5664, 29183)
for time in range(0, len(load.power)):
    load_power = load.power[time]
    load_energy = load.energy[time]
    pv_power = pvarray.power[time]
    pv_energy = pvarray.energy[time]
#    power_algorithm1(load_power, load_energy, pv_power, pv_energy,
#                     load, pvarray, batterypack, fte, grid)
#def power_algorithm_1(load_power, load_energy, pv_power, pv_energy, load, pvarray, batterypack, fte, grid):
    #Case 1: P_Load > P_PV: fully use PV power and discharge battery and/or FTE
    if load_power >= pv_power:
        rest_power = load_power - pv_power
        rest_energy = rest_power * conv_factor
        #Battery update
        if batterypack.soc > batterypack.min_soc: #Battery can be used because energy left
            #The max power to deliver in the next 15 min is the min of the resting power,
            #the maximum discharge power and the power to discharge to the min in the next 15 min
            batterypack.power = min(rest_power, batterypack.max_discharge,
                                    (batterypack.soc - batterypack.min_soc)/conv_factor)
        else:
            batterypack.power = 0
        batterypack.discharge(batterypack.power * conv_factor)
        rest_power -= batterypack.power
        rest_energy -= batterypack.power * conv_factor
        #FTE update
        if (rest_power > 0 and fte.soc > fte.min_soc): #Need to use FTE and can be used because still energy
            fte.power = min(rest_power, fte.max_discharge, (fte.soc - fte.min_soc)/conv_factor)
        else:
            fte.power = 0
        fte.discharge(fte.power * conv_factor)
        rest_power -= fte.power
        rest_energy -= fte.power * conv_factor
        #Grid update
        if rest_power > 0: #Still power needed --> grid supplies all rest power
            grid.power = rest_power
            grid.prod += grid.power * conv_factor
        else:
            grid.power = 0
    #Case 2: P_Load < P_PV: charge battery and/or fte with excess PV power
    else:
        excess_power = pv_power - load_power
        excess_energy = excess_power * conv_factor
        #Battery update
        if batterypack.soc < batterypack.max_soc: #Battery can be charged because not full yet
            #Take power positive as outgoing of component: STILL CONFUSING
            batterypack.power = - min(excess_power, batterypack.max_charge,
                                      (batterypack.max_soc - batterypack.soc)/conv_factor)
        else:
            batterypack.power = 0
        batterypack.charge(-batterypack.power * conv_factor)
        excess_power += batterypack.power
        excess_energy += batterypack.power * conv_factor
        #FTE update
        if (excess_power > 0 and fte.soc < fte.max_soc):
            fte.power = - min(excess_power, fte.max_charge, (fte.max_soc - fte.soc)/conv_factor)
        else:
            fte.power = 0
        fte.charge(-fte.power * conv_factor)
        excess_power += fte.power
        excess_energy += fte.power * conv_factor
        #Grid update
        if excess_power > 0:  # Still power excess --> grid consumes excess
            grid.power = - excess_power  # Grid consumes everything else
            grid.cons -= grid.power * conv_factor  # Total consumed by grid increases
        else:
            grid.power = 0

    #Update variables for output plots
    bat_power_level.append(batterypack.power)
    bat_soc.append(batterypack.soc)
    fte_power_level.append(fte.power)
    fte_soc.append(fte.soc)
    grid_power_level.append(grid.power)
    grid_prod_total.append(grid.prod)
    grid_cons_total.append(grid.cons)

'''Plotting resulting soc and power levels of simulation'''
plt.subplot(3,2,1)
plt.plot(load.power[0:96])
plt.title('Load Power Demand')
plt.subplot(3,2,2)
plt.plot(load.energy[0:96])
plt.title('Load Energy Consumption')
plt.subplot(3,2,3)
plt.plot(bat_power_level)
plt.title('Battery Power Level')
plt.subplot(3,2,4)
plt.plot(bat_soc)
plt.title('Battery SOC')
plt.subplot(3,2,5)
plt.plot(fte_power_level)
plt.title('FTE Power Level')
plt.subplot(3,2,6)
plt.plot(fte_soc)
plt.title('FTE SOC')
plt.show()

plt.plot(grid_power_level)
plt.title('Grid Power delivery/consumption')
plt.show()

'''KPI's'''
#Percentage of load demand delivered by battery

#Percentage of load demand delivered by FTE

#Percentage of


