#Introduction to dash according to tutorial on dash.plot.ly
#In dash you create an 'application' object, which is basically your dashboard
#In this application you create a 'layout'
    #To the layout you can add 'components' (visual elements)
    #When creating a html application, you can add html components as done in the following example:
        #(More explanation in code)
'''Example one'''
import dash
import dash_html_components as html #Classic html components to add to layout (div, titles, tables,...)
import dash_core_components as dcc  #More advanced components from dash library (graphs, buttons,...)
import pandas as pd

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'] #A css style for the html page (skip details)
#
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets) #Create an application
#
#app.layout = html.Div(children=[    #Add a 'tree' of 'components' (components in components like html)
#                                        #The attribute children takes a string, a number, a component or a list of components
#    html.H1(children='Hello Dash'), #A html h1 title 'Hello Dash
#
#    html.Div(children='''
#        Dash: A web application framework for Python.
#    '''),                           #A div with 2 'children': some plain text and a graph object pre-written by dash
#
#    dcc.Graph(
#        id='example-graph',
#        figure={
#            'data': [
#                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
#                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
#            ],
#            'layout': {
#                'title': 'Dash Data Visualization'
#            }
#        }
#    )
#])
#
#if __name__ == '__main__':
#    app.run_server(debug=True)  #Html page automatically reloads when running this line again

#More advanced styles and colors can be added via the styles attribute (see online tutorial and standard html)
    #Styles are explained in chapter 2 of tutorial: https://dash.plot.ly/getting-started


'''Example 2: creating a table in dash'''
#df = pd.read_csv(
#    'https://gist.githubusercontent.com/chriddyp/'
#    'c78bf172206ce24f77d6363a2d754b59/raw/'
#    'c353e8ef842413cae56ae3920b8fd78468aa4cb2/'
#    'usa-agricultural-exports-2011.csv')
#
#def generate_table(dataframe, max_rows=10):
#    return html.Table(
#        # Header
#        [html.Tr([html.Th(col) for col in dataframe.columns])] +
#
#        # Body
#        [html.Tr([
#            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
#        ]) for i in range(min(len(dataframe), max_rows))]
#    )
#
#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#
#app.layout = html.Div(children=[
#    html.H4(children='US Agriculture Exports (2011)'),
#    generate_table(df)
#])
#
#if __name__ == '__main__':
#    app.run_server(debug=True)


'''Example 3: callback (literally: call value back from an input and use in Python program)'''
from dash.dependencies import Input, Output, State #Standard elements used in callback

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Input(id='my-id', value='initial value', type='text'),
    html.Div(id='my-div')
])

@app.callback(
    Output(component_id='my-div', component_property='children'),   #Output are the children of the component with id 'my-div'
    [Input(component_id='my-id', component_property='value')]       #Input is the value of the component with id 'my-id'
)       #Whenever the input property changes: the function is called
    #Wrapper function wraps next function and takes input from Input and outputs to Output
def update_output_div(input_value):
    return 'You\'ve entered "{}"'.format(input_value)


if __name__ == '__main__':
    app.run_server(debug=True)


'''Example 4: update value based of variables from input on button click'''
test_value = 0
#BatteryPack
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'] #CSS Style used in Dash Tutorial

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1('Personal E Simulation tool'),
    html.Div(id='Description-Box',
             children='This is a tool to simulate power consumption/production for your specific configuration.',
             style={'borderStyle':'solid'}),
    html.H3('Enter battery pack details and submit:'),
    html.Div(children=[
    html.Div(id='b1text', children='b1text'),
    dcc.Input(id='b1', placeholder='Enter # batteries', type='number', value=0),
    html.Div(id='b2text', children='b2text'),
    dcc.Input(id='b2', placeholder='Enter usable energy', type='number', value=0),
    dcc.Input(id='b3', placeholder='Enter min. energy', type='number', value=0),
    dcc.Input(id='b4', placeholder='Enter max charging power', type='number', value=0),
    dcc.Input(id='b5', placeholder='Enter max decharging power', type='number', value=0),
    dcc.Input(id='b6', placeholder='Enter initial SOC', type='number', value=0)]),
    html.Button(id='Battery button', n_clicks=0, children='Submit Battery Details'), #Define n_clicks so that callback happens when clicked
    html.Div(id='input-received',children='Not submitted')
])
#'All values are per battery', style={'fontStyle':'italic'}

#Run simulation on button click
@app.callback(
    Output(component_id='input-received', component_property='children'),
    [Input(component_id='Battery button', component_property='n_clicks')], #Can omit names of attributes
    [State('b1','value')]
)
def read_input(n_clicks,b1):
    test_value=b1
    print(test_value)
    if n_clicks ==0:
        return 'Not submitted yet'
    else:
        return 'Submitted '+str(n_clicks)+' time(s)'

if __name__ == '__main__':
    app.run_server(debug=True)