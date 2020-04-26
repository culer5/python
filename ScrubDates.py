#   Title: Scrub Dates
#  Authored by Scott Dickinson
#  Purpose: Import a file, filter data by date ranges and sort by attuid, calculate total contract value.
from functools import reduce
import pandas as pd
import numpy as np

# read in workbook and convert to dataframe
firstWorkbook = 'Accelerated SoCS TCV 20200322.xlsx'
df_info = pd.read_excel(firstWorkbook)
# With the next statement, I check the datatypes of the dataframe and I see that the column names have spaces and
# that the CLOSE MONTH column is an integer, which means I can't filter the data by date. Can be deleted
print('df_info.dtypes', df_info.dtypes)
# I clean up the column names by replacing spaces with underscores and lower case so it's consistent and easier to code
df_info.columns = \
    df_info.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')
# This statement uses the to_datetime method to convert close_month which is an int64 datatype to datetime64 object in
# order to use the close_month as a range of dates.
df_info['close_month'] = pd.to_datetime(df_info['close_month'].astype(str), format='%Y%m')
# This is just a test file to see what I got. Can be deleted.
print('df_info.dtypes', df_info.dtypes)

# Filter the dataframe for a date range and assign to new dataframes by year.
# This is for 2017
mask2017 = (df_info['close_month'] >= '2017-1-1') & (df_info['close_month'] <= '2017-12-31')
print(df_info.loc[mask2017])
grouped2017 = pd.DataFrame(df_info.loc[mask2017])
# Group the dataframe by attuid, take the mean of the months & round to 2 decimal places, rename tcv column to tcv_2017
grouped2017 = grouped2017.groupby('attuid')
groupedMean2017 = pd.DataFrame(grouped2017['tcv'].agg(np.mean).round(2))
groupedMean2017 = groupedMean2017.rename(columns={'tcv': 'tcv_2017'})
# Test file to check my result.
groupedMean2017.to_csv('mean2017Summary.csv')

# This is for 2018. Same process as 2018
mask2018 = (df_info['close_month'] >= '2018-1-1') & (df_info['close_month'] <= '2018-12-31')
grouped2018 = pd.DataFrame(df_info.loc[mask2018])
grouped2018 = grouped2018.groupby('attuid')
groupedMean2018 = pd.DataFrame(grouped2018['tcv'].agg(np.mean).round(2))
groupedMean2018 = groupedMean2018.rename(columns={'tcv': 'tcv_2018'})
# Test file to check my result
groupedMean2018.to_csv('mean2018Summary.csv')

# This is for 2019
mask2019 = (df_info['close_month'] >= '2019-1-1') & (df_info['close_month'] <= '2019-12-31')
grouped2019 = pd.DataFrame(df_info.loc[mask2019])
grouped2019 = grouped2019.groupby('attuid')
groupedMean2019 = pd.DataFrame(grouped2019['tcv'].agg(np.mean).round(2))
groupedMean2019 = groupedMean2019.rename(columns={'tcv': 'tcv_2019'})
# Test file to check my result
groupedMean2019.to_csv('mean2019Summary.csv')

# final merged dataframe with all 3 years
dfs = [groupedMean2017, groupedMean2018, groupedMean2019]
df_final = reduce(lambda left, right: pd.merge(left, right, on='attuid'), dfs)

# The last part is the variance calculation.
df_final['Variance'] = df_final['tcv_2019'] - df_final['tcv_2017']
df_final.to_csv('finalMeans.csv')
