import pandas as pd
import numpy as np
import random
import xlsxwriter

# Get data into auditing csv
auditing = pd.read_csv("Audit-Committees-Performance-Report-2020-2021.csv")

# Display all columns when printing auditing.head()
pd.set_option('display.max_columns', None)  # display all columns
# print(auditing.head())

# Drop Unnamed columns
# auditing.drop(['Unnamed: 5', 'Unnamed: 6', 'Unnamed: 7'], axis=1) # drop columns
# print(auditing.head())

# Extract column of original cap dollar values
original_cap = auditing.iloc[:, 1]
# print(original_cap)

# Replace two rows of $ - that indicate missing values with $0.00 amount
original_cap = original_cap.replace(['  $-    '], '$0.00')

# Handle dollar sign strings: get rid of $, convert string number to a float
original_cap = original_cap.replace('[\$,]', '', regex=True).astype(float)

# Convert original_cap Series to a numpy array
original_cap_array = original_cap.values
writer = pd.ExcelWriter('./NewData.xlsx', engine='xlsxwriter')
original_cap_generated = []
for row in original_cap_array:
    original_cap_generated.append(np.random.normal(row, 0.10*row))
spending_generated = []
for row in original_cap_array:
    fixed_cost = row * 0.2
    spending_generated.append(np.random.normal(
        (row - fixed_cost), 0.25*(row - fixed_cost)))

# List comprehension version in case there's a lot of data in the future
# original_cap_generated = [original_cap_generated.append(np.random.normal(row, 0.10*row)) for row in original_cap_array]

# Round floats to 2 decimal points up
for i in range(len(original_cap_generated)):
    original_cap_generated[i] = round(original_cap_generated[i], 2)
for i in range(len(spending_generated)):
    spending_generated[i] = round(spending_generated[i], 2)


print(original_cap_generated)  # final rounded data
print(spending_generated)

# Make a dataframe out of original_cap_generated
original_cap_data = pd.DataFrame(original_cap_generated, columns=[
                                 'Original Cap Generated Data'])

# Make a dataframe out of spending_generated
spending_data = pd.DataFrame(spending_generated, columns=[
                             'Spending Cap Generated Data'])

# Get club name of clubs to add before the spending_generated and original_cap columns
club_names = auditing.iloc[:, 0]
print(club_names)

club_names_df = pd.DataFrame(club_names, columns=['Club'])

frames = [club_names_df, original_cap_data, spending_data]
# concatenate the two dataframes together by column to prevent NaN from appearing
all_data = pd.concat(frames, axis=1)

print(all_data.head())

all_data.to_csv('Sheet1.csv', index=False)
# all_data.to_excel("Sheet1.xlsx") I don't have Excel installed on my laptop so this doesn't work but it should if you have Excel installed
