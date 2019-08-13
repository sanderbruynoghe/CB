# Simul_v1.py
'''Script for running a simulation on a house with different partial loads,
a battery, a FuelCell-Tank-Electrolyzer and solar panels'''
import pandas as pd
from SimulElem_v4 import *

'''Parameters to control'''

# Loads and PV data excels:
    # Different excels for different day scenario's (TO DO)
    # Eventually put togehther in one big dataframe:
loads_data = pd.read_excel('Loads_data_house.xlsx')         # Final simulation data
pv_data = pd.read_excel('PV_data_house.xlsx')               # Final simulation data
timestep = 60*5                                             # Time step used in data [s]
conv_factor = time_interval/(60*60)     #x kW for time_interval sec: x*time_interval/(60*60) kWh energy used in interval
# Batteries
battery_data = {'RESU10H':{'MaxCh':5, 'MaxDisCh':5, 'MaxSoc':9.3}}
battery_list = {'RESU10H':3}

# FuelCell - Tank - Electrolyzer
    # Tank
tank_max_level = 100
# tank_init_level = #Optional
    # Fuel Cell
fc_max_power = 2.4
fc_efficiency = 0.33
    # Electrolyzer
el_max_power = 5
el_efficiency = 0.33

'''Initialize components'''
# Load(s)
loads_pp = {name:max(loads_data[name]) for name in loads_data.columns.values[1:]}
loads_ppp = 60*5    # TO DO (derive from data)
    # Initialize loads and put in dictionary
loads_dict = {name:Load(name, loads_pp[name], loads_ppp) for name in loads_data.columns.values[1:]}
print(loads_dict)
print(loads_dict.values())
# PV Array(s)
    # Initialize PV arrays and put in dictionary
pv_dict = {name:PVArray(name) for name in pv_data.columns.values[1:]}
print(pv_dict)

# Battery(s)
battery_dict  = {}
for bat_name, nr in battery_list.items():
    for i in range(nr):
        battery_dict[bat_name +'_'+ str(i+1)] = Battery(battery_data[bat_name]['MaxCh'],
                                         battery_data[bat_name]['MaxDisCh'], battery_data[bat_name]['MaxSoc'])
print(battery_dict)

# Tank
tank = Tank(tank_max_level)

# Fuel Cell
fc = FuelCell(fc_max_power, tank, fc_efficiency)

# Electrolyzer
el = Electrolyzer(el_max_power, tank, el_efficiency)

# Grid
grid = Grid()

'''Run simulation'''
## Check data consistency:
#if len(loads_data) != len(pv_data):
#    raise Exception('No equal length load and pv data')
#
## Actual simulation
#for time in range(len(loads_data)):
#    # Determine current power levels of loads and pv:
#    for name,load in loads_dict.items():
#        load.power = loads_data[name][time]
#    for name,pvarray in pv_dict.items():
#        pvarray.power = pv_data[name][time]
#    # Use algorith to decide over future
#    PowerAlgorithm1(loads_dict, pv_dict, battery_dict, tank, fc, el, grid, timestep)
#    SimulProgress.save(loads_dict, pv_dict, tank, fc, el, grid)
#
#SimulProgress.plot_results()


