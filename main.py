#pywinauto manual, https://readthedocs.org/projects/airelil-pywinauto/downloads/pdf/latest/

# working test
# app = Application().start("notepad.exe")
#
# app.UntitledNotepad.menu_select("Help->About Notepad")
# app.AboutNotepad.OK.click()
# app.UntitledNotepad.Edit.type_keys("pywinauto Works!", with_spaces = True)

from pywinauto import Desktop, Application, mouse, findwindows
import pywinauto
import subprocess
import time
from pywinauto.controls.uiawrapper import UIAWrapper
from pywinauto.keyboard import send_keys
from pywinauto import backend
import pandas as pd
import numpy as np
import datetime
import yfinance as yf
import csv

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

save_path = "D:\\Trash\\unusual_options_output.csv"

# Skip first 5 filler rows in CSV file
df = pd.read_csv(save_path, skiprows=5)

#print(df)
ticker_list = df['Symbol'].tolist()
sorted(set(ticker_list)) #alphabetize and remove duplicates
print(ticker_list)

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
        #print(df_all_expirations_list) #to see all expirations
        #add loop here to get each expirations options
        appended_data = []
        for specificExpirationDay in df_all_expirations_list:
            data = tk.option_chain(specificExpirationDay)
            #data is a bunch of dataframes. Just going to focus on df[0] for now.
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
            print('Current ticker processing:')
            print(each_ticker)
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
        big_dataframe_one_ticker = pd.concat(appended_data)
    except:
        pass
big_dataframe_all_tickers = pd.concat(big_dataframe_one_ticker)

print(big_dataframe_all_tickers)


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
#     # Drop unnecessary and meaningless columns
#     options = options.drop(
#         columns=['contractSize', 'currency', 'change', 'percentChange', 'lastTradeDate', 'lastPrice'])
#
#     return options
#
# #options_chain(ticker_list)
# print(options_chain("WLTW" "ADCT"))
############################################################