#   Title: Scrub Dates
#  Authored by Scott Dickinson
#  Purpose: XXXXXXX
import pandas as pd

# read in workbook and convert to dataframe
firstWorkbook = 'Accelerated SoCS TCV 20200322.xlsx'
df_info = pd.read_excel(firstWorkbook)
# With the next statement, I check the datatypes of the dataframe and I see that the column names have spaces and
# that the CLOSE MONTH column is an integer, which means I can't filter the data by date.
print(df_info.dtypes)
print(df_info)
# I clean up the column names by replacing spaces with underscores and lower case so it's consistent and easier to code
df_info.columns = \
    df_info.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')
df_info['close_month'] = pd.to_datetime(df_info['close_month'].astype(str), format='%Y%m')
# This is just a test file to see what I got. Can be deleted.
df_info.to_excel("scrubbed.xlsx")
# Filter the dataframe for a date range and assign to a new dataframe.
df_clean_2017 = df_info[
    (df_info.close_month > pd.Timestamp(2017, 1, 1)) & (df_info.close_month <= pd.Timestamp(2017, 12, 31))]

print(df_clean_2017)
