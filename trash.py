from datetime import datetime, date, timedelta
import pandas as pd

today = datetime.now()
# timespan = timedelta(days=5)
# today_plus_5days = today + timespan
# today_minus_5days = today - timespan
#
# print("Today's date:", today_plus_5days)
#
# nyse = mcal.get_calendar('NYSE')
#
# print(nyse.valid_days(start_date='2021-12-20', end_date='2022-01-10'))

def is_business_day(date):
    return bool(len(pd.bdate_range(date, date)))
print(is_business_day(today))