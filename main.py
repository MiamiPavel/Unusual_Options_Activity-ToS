#pywinauto manual, https://readthedocs.org/projects/airelil-pywinauto/downloads/pdf/latest/

#from pywinauto.controls.uiawrapper import UIAWrapper
#from pywinauto.keyboard import send_keys
#from pywinauto import backend
#from pywinauto import Desktop, Application, mouse, findwindows #REMOVE Hashtag when on Windows
import pandas as pd
import numpy as np
import yfinance as yf
from Gmail_Api.Gmail_RetrieveEmails import *
import yagmail #use this to send email out. It is 1000 times easier than native gmail solution
from datetime import datetime
from config import * #passwords and api info should live here and be .gitignore listed

print(ticker_list)

# use for testing
#save_path = "unusual_options_output.csv"

# Skip first 5 filler rows in CSV file
#df = pd.read_csv(save_path, skiprows=3) #Headers are on row 6.

#print(df)
#ticker_list = df['Symbol'].tolist()
# ^ use for testing


sorted(set(ticker_list)) #alphabetize list

deduped_ticker_list = []
for i in ticker_list: #remove duplicates from list
    if i not in deduped_ticker_list:
        deduped_ticker_list.append(i)

ticker_list = deduped_ticker_list

print(ticker_list)
#print("ticker_list type:")
#print(type(ticker_list))

appended_data = []
options_df = []
# --------- End section download from ToS -------------
for each_ticker in ticker_list:
    try:
        tk = yf.Ticker(each_ticker)
        expirations = tk.options
        # yfinance stopped supplying an expirationdate column.
        # Going to pull it from first column
        df_all_expirations_list = pd.DataFrame(data=expirations, columns=['allExpirationDatesList'])
        # Make expiration dates into a list so that we can use it to loop
        df_all_expirations_list = df_all_expirations_list['allExpirationDatesList'].tolist()
        print("OuterLoop Checkpoint A")
        #print(df_all_expirations_list) #to see all expirations
        #add loop here to get each expirations options
        for specificExpirationDay in df_all_expirations_list:
            data = tk.option_chain(specificExpirationDay)
            #data is a bunch of dataframes. Just going to focus on df[0] for now.
            print("InnerLoop Checkpoint 1")
            df = data[0]
            slicepoint = []
            tickerLength = len(each_ticker)
            if tickerLength == 1:
                slicepoint = slice(1, 7)
            elif tickerLength == 2:
                slicepoint = slice(2, 8)
            elif tickerLength == 3:
                slicepoint = slice(3, 9)
            elif tickerLength == 4:
                slicepoint = slice(4, 10)
            elif tickerLength == 5:
                slicepoint = slice(5, 11)
            elif tickerLength == 6:
                slicepoint = slice(6, 12)
            print("InnerLoop Checkpoint 2")
            print('Current ticker processing:')
            print(each_ticker)
            # Split the first column to get out date
            expirationDate = df["contractSymbol"].str[slicepoint]
            # Add column to dataframe
            df['Ticker'] = each_ticker
            df['expirationDate'] = expirationDate
            print("InnerLoop Checkpoint 3")
            # Change column formatting to date
            df['expirationDate'] = pd.to_datetime(df['expirationDate'], format='%y%m%d')
            # store DataFrame in list
            appended_data.append(df)
            print("InnerLoop Checkpoint 4")
            #print("appended_data.append(df):")
            #print(type(appended_data))
            #print(appended_data)
        # see pd.concat documentation for more info
        # pd.concat turns that list of dataframes into a single dataframe
        options_df = pd.concat(appended_data)
        print("OuterLoop Checkpoint B")
        #print("big_dataframe_one_ticker:") # remove hashtag if need to Git_Gmail_Module
        #print(type(big_dataframe_one_ticker))
        #print(big_dataframe_one_ticker)
    except:
        print("ERROR: Exception")
        pass

# Drop unnecessary and meaningless columns
options_df = options_df.drop(
         columns=['contractSize', 'currency'])

# Multiply Filled Price by Volume
options_df['dollarsTradedTodayApprox'] = options_df['strike'] * options_df['volume']
options_df['dollarsTradedTodayApprox'] = options_df['dollarsTradedTodayApprox'].astype(float)

# Remove NaN values
options_df['volume'].replace('', np.nan, inplace=True) # replace empty with Nan
options_df.dropna(subset=['volume'], inplace=True) # drop rows that have no volume

# Sort Column Descending
options_df.sort_values(by=['dollarsTradedTodayApprox'], inplace=True, ascending=False)

# To have second export as pivot table.
#options_df_byTicker = pd.pivot_table(options_df, values='dollarsTradedTodayApprox', index=['Ticker',  aggfunc=np.sum)

# Make as pivot and sort descending
#options_df_byTicker.sort_values(by=['dollarsTradedTodayApprox'], inplace=True, ascending=False)
options_df_byTicker = pd.pivot_table(options_df,index=['Ticker'],values=['dollarsTradedTodayApprox'],aggfunc=np.sum)
options_df_byTicker.sort_values(by=['dollarsTradedTodayApprox'], inplace=True, ascending=False)

# Format column 'dollarsTradedTodayApprox' as a currency string with no decimal
options_df['dollarsTradedTodayApprox'] = options_df['dollarsTradedTodayApprox'].apply('${:,}'.format)
options_df_byTicker['dollarsTradedTodayApprox'] = options_df_byTicker['dollarsTradedTodayApprox'].apply('${:,}'.format)

### This block was giving error
# Format column 'dollarsTradedTodayApprox' as a currency string with no decimal
#options_df_byTicker['dollarsTradedTodayApprox'] = options_df_byTicker['dollarsTradedTodayApprox'].astype(float) #convert to float
#options_df_byTicker['dollarsTradedTodayApprox'] = options_df['dollarsTradedTodayApprox'].apply('${:.0f}'.format) #add $ sign
###

# format contractSymbol column to be able to paste in ThinkOrSwim
options_df['contractSymbol'] = options_df['contractSymbol'].str.replace('000','') # replace 3 zeros in 2 different places
options_df['contractSymbol'] = options_df['contractSymbol'].str.replace('C00','C') # another small fix replacement
options_df['contractSymbol'] = '.' + options_df['contractSymbol'].astype(str) # Add '.' as prefix

print("Options:")
print(options_df)
print(options_df_byTicker)

# Export To Excel File with number formatting of 'dollarsTradedTodayApprox'
options_df.to_excel(r'FinalOutput-By_Options_Contract.xlsx', index = False)
writer = pd.ExcelWriter('FinalOutput-By_contract.xlsx',
                       engine='xlsxwriter',
                       options={'strings_to_numbers': True})

options_df_byTicker.to_excel(r'FinalOutput-By_Ticker.xlsx')
writer = pd.ExcelWriter('FinalOutput-By_Ticker.xlsx',
                       engine='xlsxwriter',
                       options={'strings_to_numbers': True})


# pulled from a medium article, https://medium.com/@txlian13/webscrapping-options-data-with-python-and-yfinance-e4deb0124613
#############################################################
# def options_chain(symbol):
#     tk = yf.Ticker(symbol)
#     # Expiration dates
#     all_expirations_list = tk.options
#     df = all_expirations_list
#
#     # yfinance stopped supplying an expirationdate column.
#     # Going to pull it from first column
#     df['expirationdate'] = df['contractSymbol'].str.slice(4, 6)
#
#     # Get options for each expiration
#     options = pd.DataFrame()
#
#
#     for specific_expiration in all_expirations_list:
#         opt = tk.option_chain(specific_expiration)
#         opt = pd.DataFrame().append(opt.calls).append(opt.puts)
#         opt['expirationDate'] = specific_expiration
#         options = options.append(opt, ignore_index=True)
#
#     # Bizarre error in yfinance that gives the wrong expiration date
#     # Add 1 day to get the correct expiration date
#     options['expirationDate'] = pd.to_datetime(options['expirationDate']) + datetime.timedelta(days=1)
#     options['dte'] = (options['expirationDate'] - datetime.datetime.today()).dt.days / 365
#
#     # Boolean column if the option is a CALL
#     options['CALL'] = options['contractSymbol'].str[4:].apply(
#         lambda x: "C" in x)
#
#     options[['bid', 'ask', 'strike']] = options[['bid', 'ask', 'strike']].apply(pd.to_numeric)
#     options['mark'] = (options['bid'] + options['ask']) / 2  # Calculate the midpoint of the bid-ask
#
#
#
#     return options
#
# #options_chain(ticker_list)
# print(options_chain("WLTW" "ADCT"))
############################################################

# Format todays date for insertion in emails
today = datetime.now().strftime("%Y-%m-%d")

# Send two emails. I couldn't send one with both.
# Send email functionality

yag = yagmail.SMTP("plitv001@gmail.com",gmailpass)
receiver = ["plitv001+stock@gmail.com","honnoratgabriel@gmail.com","rxjoshua@gmail.com","vp2345@gmail.com"]

for x in receiver: #loop to send to all in the receiver list
    subject = str(today) + " Unusual Stock Options Activity for Today - By Ticker"
    body = options_df
    yag.send(
        to=receiver[x],
        subject=subject,
        contents=body)
    print("Email Sent")

    # Send email functionality
    subject = str(today) + " Unusual Stock Options Activity for Today - By Ticker"
    body = options_df_byTicker
    yag.send(
        to=receiver[x],
        subject=subject,
        contents=body)
    print("Email Sent")