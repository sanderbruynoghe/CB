import pandas as pd

loads_data = pd.read_excel('Loads_data_house.xlsx')         # Final simulation data

print(loads_data['NIBE'][0])