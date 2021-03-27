#pywinauto manual, https://readthedocs.org/projects/airelil-pywinauto/downloads/pdf/latest/

#from pywinauto.controls.uiawrapper import UIAWrapper
#from pywinauto.keyboard import send_keys
#from pywinauto import backend
#from pywinauto import Desktop, Application, mouse, findwindows #REMOVE Hashtag when on Windows
import pandas as pd
import numpy as np
import yfinance as yf

# # ------ Section: Download CSV from ToS ------------------
#
# app = Application(backend='uia').start(r"C:\Program Files\thinkorswim\thinkorswim.exe")
#
# time.sleep(15)
#
# TOS_app=app.window(title="Logon to thinkorswim")
#
# userid='PLitv001 /n'
# password='Rtbd200{%}'
#
# top_window = app.window(title_re="Logon to thinkorswim", visible_only=False)
# wrp= TOS_app.wrapper_object()
# wrp.click_input()
# time.sleep(2)
# wrp.type_keys(password)
# time.sleep(2)
# send_keys('{VK_RETURN}')
# time.sleep(0.5)
# send_keys('{VK_RETURN}')
#
# time.sleep(15)
#
# #menu select not working. Hotkey does. ^ symbol is hold control down. % is alt key. + is shift key.
# send_keys('^4')
#
#
# # The ThinkOrSwim app is like a webapplet. You can't select individual elements.
#
# # time.sleep(1)
# #
# # TOS_app=app.window(title="Paper@thinkorswim *")
# #
# # pane = UIAWrapper(TOS_app.element_info)
# # TOS_app.print_control_identifiers()
#
# # send_keys('{VK_RETURN}')
# # #TOS_app.menu_select("Scan")
# # TOS_app.menu_select("Analyze")
#
# # Going to click screen coordinates instead
#
# #!!! Dont forget to filter out stocks that have earnings coming. It could just be a run up.
# # On paper accounts, TD doesn't allow Studies filter that has ability to filter these out.
# # I didn't want to have this work on the Live Account
#
# # Scan button click
# coordinate1 = 1890
# coordinate2 = 300
# pywinauto.mouse.move(coords=(coordinate1, coordinate2))
# pywinauto.mouse.click(button='left', coords=(coordinate1, coordinate2))
# time.sleep(1)
#
# # dropdown button click
# coordinate1 = 1896
# coordinate2 = 63
# pywinauto.mouse.move(coords=(coordinate1, coordinate2))
# pywinauto.mouse.click(button='left', coords=(coordinate1, coordinate2))
# time.sleep(1)
#
# # dropdown "Export" button click
# coordinate1 = 1896
# coordinate2 = 234
# pywinauto.mouse.move(coords=(coordinate1, coordinate2))
# pywinauto.mouse.click(button='left', coords=(coordinate1, coordinate2))
# time.sleep(1)
#
# # dropdown "CSV" button click
# coordinate1 = 1664
# coordinate2 = 235
# pywinauto.mouse.move(coords=(coordinate1, coordinate2))
# pywinauto.mouse.click(button='left', coords=(coordinate1, coordinate2))
# time.sleep(1)
#
# save_path = "D:\\Trash\\unusual_options_output.csv"
#
# # path where to save
# time.sleep(2)
# send_keys(save_path)
# time.sleep(1)
# send_keys('{VK_RETURN}')
# time.sleep(1)
# send_keys('{VK_RETURN}') #overwrite
#
# # Close ToS
# coordinate1 = 1897
# coordinate2 = 16
# pywinauto.mouse.move(coords=(coordinate1, coordinate2))
# pywinauto.mouse.click(button='left', coords=(coordinate1, coordinate2))
# time.sleep(1)
# send_keys('{VK_RETURN}')


save_path = "unusual_options_output.csv"

# Skip first 5 filler rows in CSV file
df = pd.read_csv(save_path, skiprows=3) #Headers are on row 6.

#print(df)
ticker_list = df['Symbol'].tolist()
sorted(set(ticker_list)) #alphabetize and remove duplicates
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

# Format column 'dollarsTradedTodayApprox' as a currency string with no decimal
options_df['dollarsTradedTodayApprox'] = options_df['dollarsTradedTodayApprox'].apply('${:.0f}'.format)

# To have second export as pivot table.
#options_df_byTicker = pd.pivot_table(options_df, values='dollarsTradedTodayApprox', index=['Ticker',  aggfunc=np.sum)

# Sort Column Descending
#options_df_byTicker.sort_values(by=['dollarsTradedTodayApprox'], inplace=True, ascending=False)
options_df_byTicker = pd.pivot_table(options_df,index=['Ticker','contractSymbol'],values=['dollarsTradedTodayApprox'],aggfunc=np.sum)


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