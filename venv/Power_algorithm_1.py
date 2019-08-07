#Power_algorithm_1.py
'''Power algorithm 1'''
def pa1(load_power, load_energy, pv_power, pv_energy, load, pvarray, batterypack, fte, grid, conv_factor):
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