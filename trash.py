
import pandas as pd
import numpy as np
import yfinance as yf
import datetime

pd.set_option('display.max_columns', None)

symbol = 'WLTW'

tk = yf.Ticker(symbol)
expirations = tk.options
df_all_expirations_list = pd.DataFrame(data=expirations, columns=['allExpirationDatesList'])

# Make expiration dates into a list so that we can use it to loop
df_all_expirations_list = df_all_expirations_list['allExpirationDatesList'].tolist()

#print(df_all_expirations_list) #to see all expirations

#add loop here to get each expirations options
appended_data = []
for specificExpirationDay in df_all_expirations_list:
    data = tk.option_chain(specificExpirationDay)
    #data is a bunch of dataframes. Just going to focus on df[0] for now.
    df = data[0]
    slicepoint = []
    tickerLength = len(symbol)
    if tickerLength == 1:
        slicepoint = slice(1,7)
    elif tickerLength == 2:
        slicepoint = slice(2,8)
    elif tickerLength == 3:
        slicepoint = slice(3,9)
    elif tickerLength == 4:
        slicepoint = slice(4,10)
    print(slicepoint)
    # Split the first column to get out date
    expirationDate = df["contractSymbol"].str[slicepoint]
    # Add column to dataframe
    df['expirationDate'] = expirationDate
    # Change column formatting to date
    df['expirationDate'] = pd.to_datetime(df['expirationDate'], format='%y%m%d')
    # store DataFrame in list
    appended_data.append(df)
# see pd.concat documentation for more info
# pd.concat turns that list of dataframes into a single dataframe
appended_data = pd.concat(appended_data)

print(appended_data)




