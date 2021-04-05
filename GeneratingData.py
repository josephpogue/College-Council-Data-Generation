import pandas as pd
import numpy as np
import random

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

original_cap_generated = []
for row in original_cap_array:
    original_cap_generated.append(np.random.normal(row, 0.10*row))
spending_generated = []
for row in original_cap_array:
    fixed_cost = row * 0.2
    spending_generated.append(np.random.normal(
        (row - fixed_cost), 0.5*(row - fixed_cost)))

# List comprehension version in case there's a lot of data in the future
# original_cap_generated = [original_cap_generated.append(np.random.normal(row, 0.10*row)) for row in original_cap_array]

# Round floats to 2 decimal points up
for i in range(len(original_cap_generated)):
    original_cap_generated[i] = round(original_cap_generated[i], 2)
for i in range(len(spending_generated)):
    spending_generated[i] = round(spending_generated[i], 2)

print(original_cap_generated)  # final rounded data
print(spending_generated)
