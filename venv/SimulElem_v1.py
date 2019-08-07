#SimulElem_v1.py
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

'''Model Objects'''

class Load():

    def __init__(self):
        load_2018 = pd.read_excel('Consumption_data.xlsx') #For now: just SLP from VREG with 13000 kWh year consumption
            #4 columns: Date_Time, S21, Consump_Energy_est, Consump_Power_est with 35036 data points
        self.data = load_2018
        self.power = self.data.Consump_Power_est
        self.energy = self.data.Consump_Energy_est
        self.date_time  =self.data.Date_Time

class BatteryPack():

    def __init__(self, number_of_batt, max_energy_one, min_energy_one, charge_discharge_power_one, init_energy):
        self.b = number_of_batt
        self.cap = max_energy_one * number_of_batt
        self.min = min_energy_one * number_of_batt
        self.max_charge = charge_discharge_power_one * number_of_batt #Max charge power,ASSUMED: linear in number of batteries
        self.max_discharge = self.max_charge #ASSUMED: charge and discharge rate equal
        self.soc = init_energy #ASSUMED: for total pack
        self.power = 0 #Initialize battery as (dis)charging with zero power

    def charge(self, energy):
        self.soc += energy

    def discharge(self, energy):
        self.soc -= energy

    def update_power(self, new_power):
        self.power = new_power

class PVArray():

    def __init__(self, number_of_pv, Wp):
        self.wp = Wp
        self.p = number_of_pv
        prod_2018 = pd.read_excel('PV_Prod_data.xlsx')
        self.data = prod_2018
        self.power = self.data.PV_Power_est * number_of_pv #Power delivered during each 15 mins
        self.energy = self.data.PV_Energy_est * number_of_pv #Energy generated during each 15 mins

class FuelTankElectrolyzer():

    def __init__(self, max_energy, min_energy, elec_to_tank, tank_to_elec, charge_power, discharge_power, init_energy):
        self.cap = max_energy
        self.min = min_energy
        self.alpha = elec_to_tank
        self.beta = tank_to_elec
        self.max_charge = charge_power
        self.max_discharge = discharge_power
        self.soc = init_energy
        self.power = 0 #Initialize FTE as delivering zero power

    def charge(self, energy):
        self.soc += energy

    def discharge(self, energy):
        self.soc -= energy

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

