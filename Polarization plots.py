#code to make polarization plot
#import packages

#read
import os
import pandas as pd
import matplotlib.pyplot as plt
#where files live
folder_path = 'C:/Users/L136_L2/Documents/8262026'
#list all csv files in the folder
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
#read and concatenate data:loop through each csv file, read it into a pandas data frame and append it into a list
all_dataframes = []
for csv_file in csv_files:
    file_path = os.path.join(folder_path, csv_file)
    df = pd.read_csv(file_path)
    all_dataframes.append(df)

combined_df = pd.concat(all_dataframes, ignore_index=True)

#convert to a numpy array
data_array = combined_df.values
print(data_array)
plt.plot(data_array)