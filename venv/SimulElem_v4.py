#SimulElem_v4.py
'''Script containing all basic units from the simulation and implementation.
Different loads and the other components can be initialized when starting a simulation.
The algorithm for controlling these components is defined elsewhere.'''
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time

'''Model Objects'''

class Load():
    '''General load class'''
    def __init__(self, name, pp, ppp):
        self.name = name                    # Name of load in Smappee
        self.power = 0                      # Current power reading of load
        self.forecast = 0                   # Upcoming forecast of power demand
        #self.status = ...                  # On or off depending on control algorithm
            #Power must be 0 when status = off
            #Will need new function: set_status
            #How to implement in simulation?

    def power_read(self):
        '''Function reading and updating the power consumption of a component'''
        # For simulation: not used
        return self.power
        # Actual implementation: constantly update value via Smappee



    def load_forecast(self):
        '''Function providing power forecast for the next period [kW in every 5 min]'''
        # For simulation: based on current time in simulation
        return 0
        # Actual implementation: based on actual time at this moment

class PVArray():
    '''PV Array class'''
    def __init__(self, name):
        self.name = name                    # Name of PV array
        self.power = 0                      # Current power reading of pv array
        self.forecast = 0                   # Upcoming forecast of PV production

    def power_read(self):
        '''Function reading and updating the power production of the pv'''
        # For simulation: not used
        return self.power
        # Actual implementation: constantly update value via Smappee

    def pv_forecast(self):
        '''Function providing power forecast for the next period [kW in every 15 min]'''
        # For simulation: based on current time in simulation
        return 0
        # Actual implementation: based on actual time at this moment


class Battery():
    '''Battery class'''
    def __init__(self, max_charge, max_discharge, max_soc, init_soc = 0):
        self.max_charge = max_charge                        # Max charging power [kW]
        self.max_discharge = max_discharge                  # Max discharging power [kW]
        self.max_soc = max_soc                              # Max. energy stored in battery [kWh]
        self.soc = init_soc                                 # Current SOC level of battery
        self.power = 0                                      # Current battery power level
            # Power is pos. (>0) when battery delivers power, neg. (<0) when consuming power (charging)

    def soc_read(self):
        '''Funtion reading and updating the energy stored in the batterypack (SOC)'''
        # For simulation: not used
        return self.soc
        # Actual implementation: constantly update value

    def batt_power_read(self):
        '''Funtion reading and updating the Battery power'''
        # For simulation: not used
        return self.power
        # Actual implementation: constantly update value via Smappee

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
    def __init__(self, max_level, min_level = 0, init_level = 0):
        self.max_level = max_level          # Max H2 level in the tank [kg]
        self.min_level = min_level
        self.level = init_level             # Current H2 level [kg]

    def level_read(self):
        '''Funtion reading and updating the Tank H2 level'''
        # For simulation: not used
        return self.level
        # Actual implementation: constantly update value via Smappee

    def charge(self, h2):
        '''Load tank with h2 [kg]'''
        self.level += h2

    def discharge(self, h2):
        '''Unload tank with h2 [kg]'''
        self.level -= h2


class FuelCell():
    '''Fuel Cell class'''
    def __init__(self, max_power, tank, efficiency):
        self.max_power = max_power          # Max possible power delivery
        self.tank = tank                    # Tank connected to fuel cell
        self.efficiency = efficiency        # kWh produced / kg H2
        self.power = 0                      # Current power output level
        # self.des_power = ...              # Desired power level

    def fc_power_read(self):
        '''Funtion reading and updating the Fuel Cell Power output'''
        # For simulation: initially set power to zero
        return self.power
        # Actual implementation: constantly update value via Smappee

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
        self.tank = tank                    # Tank connected to electrolyzer
        self.efficiency = efficiency        # kWh consumed / kg H2
        self.max_power = max_power          # Max possible power consumption
        self.power = 0                      # Current power output level
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
        self.power = 0                      # Power level of the grid
            #Power is pos. (>0) when grid delivers power, neg. (<0) when consuming power

    def grid_read_power(self):
        '''Funtion reading and updating the Grid power'''
        # For simulation: initially set power to zero
        return 0
        # Actual implementation: measurements from Smappee


