#code to make polarization plot
#import packages

import os
import pandas as pd
import matplotlib.pyplot as plt

# Path to your folder with CSV files
folder_path = "C:/Users/L136_L2/Documents/8262026"

# Get list of all CSV files in the folder (sorted alphabetically)
csv_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.csv')])

# Load the first file to define x values (first column)
first_file = os.path.join(folder_path, csv_files[0])
df_first = pd.read_csv(first_file)

# Start combined dataframe with x values
combined_df = pd.DataFrame({"x": df_first.iloc[:, 0]})

# Loop through all files and add their y values as new columns
for i, file in enumerate(csv_files, start=1):
    file_path = os.path.join(folder_path, file)
    df = pd.read_csv(file_path)
    combined_df[f"y_{i}"] = df.iloc[:, 1].to_numpy()

print(combined_df.head())
plt.figure(figsize=(8, 6))

for col in combined_df.columns[1:]:  # skip the 'x' column
    plt.plot(combined_df["x"], combined_df[col], label=col)

plt.xlabel("x values")
plt.ylabel("y values")
plt.title("Combined Data from CSV Files")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

#integrate each of the y coloumns from combined_df file
import numpy as np

# Define integration limits
x_min = 15862   # set your lower bound
x_max = 16272  # set your upper bound

integrals = {}

# Apply mask to restrict to the desired x range
mask = (combined_df["x"] >= x_min) & (combined_df["x"] <= x_max)

x_range = combined_df.loc[mask, "x"].to_numpy()

for col in combined_df.columns[1:]:  # skip the 'x' column
    y_range = combined_df.loc[mask, col].to_numpy()
    integral = np.trapz(y_range, x_range)*1e20  # trapezoidal integration
    integrals[col] = integral

print(f"Integrated values from x = {x_min} to {x_max}:")
for col, val in integrals.items():
    print(f"{col}: {val}")