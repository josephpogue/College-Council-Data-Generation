import pandas as pd
import numpy as np
import random
import xlsxwriter

# Get data into auditing csv
auditing = pd.read_csv("Audit-Committees-Performance-Report-2020-2021.csv")
try:
    xlsxwriter.Workbook('NewData.xlsx')
except:
    print()

    # Display all columns when printing auditing.head()
pd.set_option('display.max_columns', None)  # display all columns

# Extract column of original cap dollar values
# iloc[row, column] - selects columns or rows in a dataframe (":" - selects all of a row or column)
original_cap = auditing.iloc[:, 1]

# Replace two rows of $ - that indicate missing values with $0.00 amount
original_cap = original_cap.replace(['  $-    '], '$0.00')

# Handle dollar sign strings: get rid of $, convert string number to a float (uses regular expressions)
original_cap = original_cap.replace('[\$,]', '', regex=True).astype(float)

# Convert original_cap Series to a numpy array
original_cap_array = original_cap.values
# Creates ExcelWriter to begin appending into an existing Excel file
writer = pd.ExcelWriter('./NewData.xlsx', mode='w', engine='openpyxl')
# Start generating numbers based on normal distribution for both budget cap and spending
original_cap_generated = []
for row in original_cap_array:
    original_cap_generated.append(round(np.random.normal(row, 0.10*row), 2))
spending_generated = []
for row in original_cap_array:
    fixed_cost = row * 0.2
    spending_generated.append(round(np.random.normal(
        (row - fixed_cost), 0.25*(row - fixed_cost)), 2))

# List comprehension version in case there's a lot of data in the future
# original_cap_generated = [original_cap_generated.append(np.random.normal(row, 0.10*row)) for row in original_cap_array]

# y1 and y2 are the sheet names (which are the years the data is generated from)
y1 = 2020
y2 = 2021
# Loop thru each sheet to write the data in it
for x in range(3):
    # Make a dataframe out of original_cap_generated
    original_cap_data = pd.DataFrame(original_cap_generated, columns=[
        'Original Cap Generated Data'])

    # Make a dataframe out of spending_generated
    spending_data = pd.DataFrame(spending_generated, columns=[
        'Spending Cap Generated Data'])
    # Extract column of all the club names
    club_names = auditing.iloc[:, 0]

    club_names_df = pd.DataFrame(club_names, columns=['Club'])
    # concatenate the two dataframes together by column to prevent NaN from appearing
    frames = [club_names_df, original_cap_data, spending_data]
    all_data = pd.concat(frames, axis=1)
    all_data.to_excel(writer, sheet_name=str(y1) + "-" + str(y2), index=False)
    # Decreases all values by 1.5%
    for i in range(len(original_cap_array)):
        original_cap_generated[i] = original_cap_generated[i] * 0.995
        spending_generated[i] = spending_generated[i] * 0.995
    y1 = y1 - 1
    y2 = y2 - 1


# all_data.to_excel("Sheet1.xlsx") I don't have Excel installed on my laptop so this doesn't work but it should if you have Excel installed
writer.save()
