import pandas as pd
import numpy as np
import random
import xlsxwriter

# Get data into auditing csv
auditing = pd.read_csv("Audit-Committees-Performance-Report-2020-2021.csv")

# Display all columns when printing auditing.head()
pd.set_option('display.max_columns', None)  # display all columns

# Extract column of original cap dollar values
original_cap = auditing.iloc[:, 1]

# Replace two rows of $ - that indicate missing values with $0.00 amount
original_cap = original_cap.replace(['  $-    '], '$0.00')

# Handle dollar sign strings: get rid of $, convert string number to a float
original_cap = original_cap.replace('[\$,]', '', regex=True).astype(float)

# Convert original_cap Series to a numpy array
original_cap_array = original_cap.values
# Creates ExcelWriter to begin appending
writer = pd.ExcelWriter('./NewData.xlsx', mode='a', engine='openpyxl')
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
x = 2020
y = 2021
for x in range(3):
    # Make a dataframe out of original_cap_generated
    original_cap_data = pd.DataFrame(original_cap_generated, columns=[
        'Original Cap Generated Data'])

    # Make a dataframe out of spending_generated
    spending_data = pd.DataFrame(spending_generated, columns=[
        'Spending Cap Generated Data'])
    club_names = auditing.iloc[:, 0]

    club_names_df = pd.DataFrame(club_names, columns=['Club'])

    frames = [club_names_df, original_cap_data, spending_data]
    # concatenate the two dataframes together by column to prevent NaN from appearing
    all_data = pd.concat(frames, axis=1)

    print(all_data.head())

    all_data.to_excel(writer, sheet_name='Sheet'+str(x), index=False)
    # Decreases all values by 1.5%
    for i in range(len(original_cap_array)):
        original_cap_generated[i] = original_cap_generated[i] * 0.995
        spending_generated[i] = spending_generated[i] * 0.995


# all_data.to_excel("Sheet1.xlsx") I don't have Excel installed on my laptop so this doesn't work but it should if you have Excel installed
writer.save()
