#SimulElem_v4.py
'''Script containing all basic units from the simulation and implementation.
Different loads and the other components can be initialized when starting a simulation.
The algorithm for controlling these components is defined elsewhere.'''
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time

'''Loads data'''
    # Dictionary containing names of loads + there consumption forecasts, peak power and peak power period
    # from data analysis
load_dict = {} #name:[peak power, expected duration]
    # Can be updated when new data is available from Smappee


'''Model Objects'''

class Load():
    '''General load class'''
    # All loads should be stored in a list (needed for other components)
    def __init__(self, name):
        self.name = name                    #Name of load
        self.pp = load_dict[name][0]        #Peak power in kW
        self.ppp = load_dict[name][1]       #Expected duration of Peak Power (Peak Power Period) [s]
        self.power = load_power_read()      #Current power reading of load
        self.forecast = load_forecast()     #Upcoming 7 days forecast of power demand
        #self.status = ...                  #On or off depending on control algorithm
            #Power must be 0 when status = off
            #Will need new function: set_status
            #How to implement in simulation?

    def load_power_read(self):
        '''Function reading and updating the power consumption of a component'''
        # For simulation: no real measurement, just take value from forecast

        # Actual implementation: readings from Smappee


    def load_forecast(self):
        '''Function providing power forecast for the next period [kW in every 15 min]'''
        # For simulation: based on current time in simulation

        # Actual implementation: based on actual time at this moment

class PVArray():
    '''PV Array class'''
    def __init__(self, panel_list):
        self.panel_list = panel_list        #List with types of pannels [Wp] and number of these pannels
            # e.g: [[330,8],[230,22]]
        self.wp = sum([panels[0]*panels[1] for panels in panel_list]) #Total Wp installed
        self.power = pv_power_read()        #Current power reading of pv array
        self.forecast = pv_forecast()       #Upcoming 7 days forecast of PV production

    def pv_power_read(self):
        '''Function reading and updating the power production of the pv'''
        # For simulation: no real measurement, just take value from forecast

        # Actual implementation: readings from Smappee

    def pv_forecast(self):
        '''Function providing power forecast for the next period [kW in every 15 min]'''
        # For simulation: based on current time in simulation

        # Actual implementation: based on actual time at this moment


class BatteryPack():
    '''Battery pack class (DOES NOT LOOK AT INDIVIDUAL BATTERIES)'''
    def __init__(self, load_dict, nr_of_batt, max_charge_one, max_discharge_one, max_soc_one, min_soc_one = 0, init_soc_one = 0):
        self.b = nr_of_batt                                 #Number of batteries in battery pack
        self.max_charge = max_charge_one * nr_of_batt       #Max charging power
            #ASSUMED: linear in number of batteries
        self.max_discharge = max_discharge_one * nr_of_batt #Max discharging power
            #ASSUMED: linear in number of batteries
        self.max_soc = max_soc_one * nr_of_batt             #Max. energy stored in battery pack [kWh]
        self.min_soc = min_soc_alg(load_dict)               #Min. energy that should be stored for power continuity [kWh]
        self.init_soc = init_soc_one * nr_of_batt           #Initial SOC of batteries
        self.soc = soc_read()                               #Current SOC level of battery
        self.power = batt_power_read()                      #Current battery power level
            # Power is pos. (>0) when battery delivers power, neg. (<0) when consuming power

    def soc_read(self):
        '''Funtion reading and updating the energy stored in the batterypack (SOC)'''
        # For simulation: just return initial SOC level
        return self.init_soc
        # Actual implementation: measurements from Smappee

    def batt_power_read(self):
        '''Funtion reading and updating the Battery power'''
        # For simulation: initially set power to zero
        return 0
        # Actual implementation: measurements from Smappee

    def min_soc_alg(self, load_dict):
        '''Function determining the required minimum SOC of the battery'''
        # Determine safety min. SOC of battery based on peak power demands from defined loads
        # For now: just set to zero
        return 0
        # Better algorithm based on peak power of loads

    def charge(self, time):
        '''Charge battery at given power level [kW] for a given time [s]. This changes the SOC.'''
        if self.power > self.max_charge:
            return 'Power overload'
        else:
            self.soc += self.power * time / (60*60)

    def discharge(self, time):
        '''Charge battery at given power level [kW] for a given time [s]. This changes the SOC.'''
        if self.power > self.max_discharge:
            return 'Power overload'
        else:
            self.soc -= self.power * time / (60*60)


class Tank():
    '''H2 Tank class'''
    def __init__(self, max_level, init_level):
        self.max_level = max_level      #Max H2 level in the tank
        self.init_level = init_level    #Initial H2 level in the tank
        self.level = level_read()       #Current H2 level

    def level_read(self):
        '''Funtion reading and updating the Tank H2 level'''
        # For simulation
        return self.init_level
        # Actual implementation: readings from Smappee

    def charge(self, h2):
        '''Load tank with h2 [kg]'''
        self.level += h2

    def discharge(self, h2):
        '''Unload tank with h2 [kg]'''
        self.level -= h2


class FuelCell():
    '''Fuel Cell class'''
    def __init__(self, max_power, tank, efficiency):
        self.tank = tank                    #Tank connected to fuel cell
        self.efficiency = efficiency        #kWh produced / kg H2
        self.max_power = max_power          #Max possible power delivery
        self.power = fc_power_read()        #Current power output level
        self.des_power = ...                #Desired power level

    def fc_power_read(self):
        '''Funtion reading and updating the Fuel Cell Power output'''
        # For simulation: initially set power to zero
        return 0
        # Actual implementation: measurements from Smappee

    def set_power(self, power):
        '''Set desired power to a given level'''
        self.des_power = power
        # For simulation: actual power = desired power
        self.power = self.des_power
        # Actual implementation: logic to control Electrolyzer

    def produce(self, time):
        '''Use H2 from tank'''
        self.tank.discharge(self.power * time / (60*60) / self.efficiency)

class Electrolyzer():
    '''Electrolyzer class'''
    def __init__(self, max_power, tank, efficiency):
        self.tank = tank                    #Tank connected to electrolyzer
        self.efficiency = efficiency        #kWh consumed / kg H2
        self.max_power = max_power          #Max possible power consumption
        self.power = electr_power_read()    #Current power output level
        self.des_power = ...                # Desired power level

    def electr_power_read(self):
        '''Funtion reading and updating the Electolyzer Power input'''
        # For simulation: initially set power to zero
        return 0
        # Actual implementation: measurements from Smappee

    def set_power(self, power):
        '''Set desired power to a given level'''
        self.des_power = power
        #For simulation: actual power = desired power
        self.power = self.des_power
        #Actual implementation: logic to control Electrolyzer

    def consume(self, time):
        '''Store H2 in tank'''
        self.tank.charge(self.power * time / (60*60) / self.efficiency)


class Grid():
    '''Grid class'''
    def __init__(self):
        self.power = grid_read_power()      #Power level of the grid
            #Power is pos. (>0) when grid delivers power, neg. (<0) when consuming power

    def grid_read_power(self):
        '''Funtion reading and updating the Grid power'''
        # For simulation: initially set power to zero
        return 0
        # Actual implementation: measurements from Smappee


