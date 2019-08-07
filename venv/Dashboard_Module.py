#Dashboard_Module.py
'''This module automatically asks user input for all necessary model parameters via a local http server'''
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import inspect
from SimulElem_v3 import *

# To update dashboard, do following steps:
    # ...

def launch_dashboard():

    # Retrieve all model parameters from SimulElem
        #MAKE SURE TO USE CORRECT VERSION OF SimulElem
    battery_params = inspect.getfullargspec(BatteryPack.__init__).args[1:] #List of all arguments from constructor except self ([1:])
    pv_params = inspect.getfullargspec(PVArray.__init__).args[1:]
    fte_params = inspect.getfullargspec(FuelTankElectrolyzer.__init__).args[1:]

    '''Setup of Dash dashboard application'''
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'] #CSS Style used in Dash Tutorial
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    #Create Dash Input elements for dashboard
    battery_inputs = [html.Div(children=[html.Div(p), dcc.Input(id=p,value=0,placeholder='Enter data here')]) for p in battery_params]
    pv_inputs = [html.Div(children=[html.Div(p), dcc.Input(id=p,value=0,placeholder='Enter data here')]) for p in pv_params]
    fte_inputs = [html.Div(children=[html.Div(p), dcc.Input(id=p,value=0,placeholder='Enter data here')]) for p in fte_params]


    #Create dash layout with Inputs and submit button
    app.layout = html.Div(children=[
        html.H1('Personal E Simulation tool'),
        html.Div(id='Description-Box',
                 children='This is a tool to simulate power consumption/production for your specific configuration.',
                 style={'borderStyle':'solid'}),
        html.Div(className='row',children=[
            html.Div(children=[html.H3('Battery Inputs'),
                               html.Div('Values are per battery',style={'fontStyle':'italic'}),
                               html.Div(battery_inputs)],className='column',style={'width':'25%'}),
            html.Div(children=[html.H3('PV Inputs'),
                               html.Div('Values are per pv panel',style={'fontStyle':'italic'}),
                               html.Div(pv_inputs)], className='column', style={'width': '25%'}),
            html.Div(children=[html.H3('FTE Inputs'),
                               html.Div('Strong simplification',style={'fontStyle':'italic'}),
                               html.Div(fte_inputs)], className='column', style={'width': '25%'}),
            ]),
        html.Div(className='row',children=[
            html.Button(id='Submit-button', n_clicks=0, children='Run Simulation', style={'align':'center'}),
                #Define n_clicks so that callback (see below) happens when clicked
            html.Div(id='Input-received',children='Not submitted')
            ])
    ])

    '''Run simulation on click'''

    #Create Dash State elements (see below):
    battery_states = [State(name,'value') for name in battery_params]
    pv_states = [State(name,'value') for name in pv_params]
    fte_states = [State(name,'value') for name in fte_params]
    total_states = battery_states + pv_states + fte_states
    print([state.component_id for state in total_states])

    @app.callback(
        Output(component_id='Input-received', component_property='children'),
        [Input(component_id='Submit-button', component_property='n_clicks')], #On change in n_clicks: execute function below
        total_states
    )
        #VERY INEFFICIENT
    def read_input(n_clicks,v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11,v12,v13,v14,v15):
        # Assign new values
        print('New values',v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11,v12,v13,v14,v15)
        number_of_batt = v1
        usable_energy_one = v2  # Usable energy of single battery [kWh]
        min_energy_one = v3  # Minimal soc level of battery (to avoid high voltage drop) [kWh]
        max_charge_bat = v4  # Max charging power (single battery) [kW]
        max_discharge_bat = v5  # Max discharging power (single battery) [kW]
        init_soc_bat = v6  # Initial state of charge of each battery [kWh]
        # PV Array: for now: 30 panels of 330 Wp (future situation of house) and production according to Elia data
        number_of_pv = v7 # Number of pv panels in array
        Wp = v8  # Peak    Power of panels [kW]
        # FuelCell-Tank-Electrolyzer combination: for now: VERY STRONG ASSUMPTIONS AND SIMPLIFICATIONS
            # Based on Intelligent Energy FCM-802 & NEL proton PEM S40
        max_soc = v9  # Max energy stored in tank [kWh]
        min_soc = v10  # Min energy stored in tank [kWh]
        fuel_cell_factor = v11  # Power conversion factor of Fuel Cell [-]
        electr_factor = v12  # Power conversion factor of Electrolyzer [-]
        # Combined: 0.57*0.57=0.33 efficiency
        max_charge_fte = v13  # Max charging power [kW]
        max_discharge_fte = v14  # Max discharging power [kW]
        init_soc_fte = v15  # Initial state of charge [kWh]: choose initially at 90% of full capacity

        # Return value
        if n_clicks == 0:
            return 'Not submitted yet'
        else:
            #run_simulation()
            return 'Simulation completed: check results'

    # Run on server
    if __name__ == '__main__':
        app.run_server(debug=True)

launch_dashboard()