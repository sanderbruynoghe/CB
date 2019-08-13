

def PowerAlgorithm1(loads_dict, pv_dict, battery_dict, tank, fc, el, grid, timestep):
    '''Simple power algorithm'''
    # Determine total load and pv power:
    load_power = sum([load.power for name, load in loads_dict.items()])
    pv_power = sum([array.power for name, array in pv_dict.items()])
    # Determine total SOC of batteries
    batteries_soc = sum([battery.soc for name, battery in battery_dict.items()])
    batteries_max_charge = sum([battery.max_charge for name, battery in battery_dict.items()])
    batteries_max_discharge = sum([battery.max_discharge for name, battery in battery_dict.items()])

    # Case 1: P_Load > P_PV: fully use PV power and discharge battery and/or FTE
    if load_power >= pv_power:
        rest_power = load_power - pv_power

        # Battery update: assume equally discharged
            # Only for simulation, because we don't actually control the battery power levels
        batteries_power = 0
        if batteries_soc > 0:
            batteries_power = min(rest_power, batteries_max_discharge, batteries_soc/conv_factor)
        for name, battery in battery_dict.items():
            battery.power = batteries_power/len(battery_dict)
            battery.discharge(timestep)
        rest_power -= batteries_power

        # Fuel Cell update:
            # Decide on Fuel Cell power level
        if rest_power > 0 and tank.level > tank.min_level:
            new_power = min(rest_power, fc.max_power,  )
            fc.set_power()

