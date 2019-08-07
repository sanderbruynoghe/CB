#SimulElem_v2.py
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

'''Model Objects'''

class Load():

    def __init__(self):
        load_2018 = pd.read_excel('Consumption_data.xlsx')
            #4 columns: Date_Time, S21, Consump_Energy_est, Consump_Power_est with 35036 data points
            #Misses last 4 data points
        self.data = load_2018
        self.power = self.data.Consump_Power_est        #Power consumed during each 15min
        self.energy = self.data.Consump_Energy_est      #Energy generated during each 15 m
        self.date_time  =self.data.Date_Time

class BatteryPack():

    def __init__(self, number_of_batt, usable_energy_one, min_energy_one, max_charge, max_discharge, init_soc):
        self.b = number_of_batt
        self.max_soc = usable_energy_one * number_of_batt
        self.min_soc = min_energy_one * number_of_batt
        self.max_charge = max_charge * number_of_batt #ASSUMED: linear in number of batteries
        self.max_discharge = max_discharge * number_of_batt
        self.soc = init_soc * number_of_batt
        self.power = 0 #Initialize battery as (dis)charging with zero power

    def charge(self, energy):
        self.soc += energy

    def discharge(self, energy):
        self.soc -= energy

class PVArray():

    def __init__(self, number_of_pv, Wp):
        self.p = number_of_pv
        self.wp = Wp
        prod_2018 = pd.read_excel('PV_Prod_data.xlsx')
        self.data = prod_2018
        self.power = self.data.PV_Power_est * number_of_pv      #Power delivered during each 15min
        self.energy = self.data.PV_Energy_est * number_of_pv    #Energy generated during each 15 mins
        self.date_time = self.data.Date_Time

class FuelTankElectrolyzer():

    def __init__(self, max_soc, min_soc, fuel_cell_factor, electr_factor, max_charge, max_discharge, init_soc):
        self.max_soc = max_soc
        self.min_soc = min_soc
        self.alpha = fuel_cell_factor
        self.beta = electr_factor
        self.max_charge = max_charge
        self.max_discharge = max_discharge
        self.soc = init_soc
        self.power = 0 #Initialize FTE as (dis)charging with zero power

    def charge(self, energy):
        self.soc += energy * self.alpha #Only alpha*energy actually stored

    def discharge(self, energy):
        self.soc -= energy / self.beta  #To deliver energy: soc decreases with energy/beta

    def update_power(self, new_power):
        self.power = new_power

class Grid():

    def __init__(self):
        # Initially the grid has delivered and 'consumed' zero energy
        self.prod = 0
        self.cons = 0
        self.power = 0 #Initialize grid as delivering zero power

    def deliver(self, energy):
        self.prod += energy

    def consume(self, energy):
        self.cons += energy

    def update_power(self, new_power):
        self.power = new_power

