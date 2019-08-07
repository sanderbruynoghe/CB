#BasicSimul_v4.py
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from SimulElem_v3 import *
from Power_algorithm_1 import *
from Dashboard_Module import *

#Stopped: put data in dictionaries

'''Parameters on dashboard'''
#Load: for now: just SLP from VREG with 13000 kWh year consumption
    #Need to find or construct better dataset later on
#System components
    #1: Battery Pack: default: 12 times 3 kWh battery
number_of_batt = 12
usable_energy_one = 3           #Usable energy of single battery [kWh]
min_energy_one = 1              #Minimal soc level of battery (to avoid high voltage drop) [kWh]
max_charge_bat = 5              #Max charging power (single battery) [kW]
max_discharge_bat = 5           #Max discharging power (single battery) [kW]
init_soc_bat = 3                #Initial state of charge of each battery [kWh]
    #2: PV Array: default: 30 panels of 330 Wp (future situation of house) and production according to Elia data
number_of_pv = 55               #Number of pv panels in array
Wp = 330                        #Peak    Power of panels [kW]
    #3: FuelCell-Tank-Electrolyzer combination: default: guessimated values based on IE FCM-802 & NEL proton PEM S40
        #Note: VERY SIMPLIFIED MODEL, certainly needs improvements
max_soc = 3500                  #Max energy stored in tank [kWh]
min_soc = 1                     #Min energy stored in tank [kWh]
fuel_cell_factor = 0.57         #Power conversion factor of Fuel Cell [-]
electr_factor = 0.57            #Power conversion factor of Electrolyzer [-]
max_charge_fte = 2.4            #Max charging power [kW]
max_discharge_fte = 2.4         #Max discharging power [kW]
init_soc_fte = 3000             #Initial state of charge [kWh]: choose initially at 90% of full capacity
    #4: Grid: for now: (dis)charging with infinite power
##Dictionaries with params:
#battery_dict = {'number_of_batt':12, 'usable_energy_one':3, 'min_energy_one': 1,
#                'max_charge_bat':5, 'max_discharge_bat':5, 'init_soc_bat':3}
#pv_dict = {'number_of_pv':55, 'Wp': 330}
#fte_dict = {'max_soc':3500, 'min_soc':1, 'fuel°cell_factor':0.57, 'electr_factor':0.57,
#            'max_charge_fte':2.4, 'max_discharge_fte':2.4, 'init_soc_fte':3000}
#Data time intervals
time_interval = 15*60                   #15*60 sec between each power measurement
conv_factor = time_interval/(60*60)     #x kW for time_interval sec: x*time_interval/(60*60) kWh energy used in interval

launch_dashboard()
'''Initialize model'''
#Load (house)
load = Load()
#System Components
batterypack = BatteryPack(di['number_of_batt'], 'usable_energy_one':3, 'min_energy_one': 1,
                'max_charge_bat':5, 'max_discharge_bat':5, 'init_soc_bat':3)
pvarray = PVArray(number_of_pv, Wp)
fte = FuelTankElectrolyzer(max_soc, min_soc, fuel_cell_factor, electr_factor,
                           max_charge_fte, max_discharge_fte, init_soc_fte)
grid = Grid()

#Arrays for storing battery, fte and grid energy and power levels
#Gym and abstract producer and consumer classes
    #Battery
bat_soc = []            #SOC at end of time slot [kWh]
bat_power_level = []    #Power level during time slot [kW]
    #FTE
fte_soc = []            #SOC at end of time slot [kWh]
fte_power_level = []    #Power level during time slot [kW]
    #Grid
grid_power_level = []   #Power level during time slot [kW]
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
    #Apply algorithm to system
    pa1(load_power, load_energy, pv_power, pv_energy,
                     load, pvarray, batterypack, fte, grid)
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
plt.plot(load.power)
plt.title('Load Power Demand')
plt.subplot(3,2,2)
plt.plot(load.energy)
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
bat_power_level_np = np.array(bat_power_level)
batt_perc = sum(bat_power_level_np[bat_power_level_np > 0])/sum(load.power)
print(batt_perc)
##Percentage of load demand delivered by FTE
#fte_perc = sum(fte_power_level[fte_power_level > 0])/sum(load.power)
#print(fte_perc)
##Percentage of load demand delivered by grid
#grid_perc = sum(grid_power_level[grid_power_level > 0])/sum(load.power)


