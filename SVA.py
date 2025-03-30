import matplotlib.pyplot as plt
import matplotlib.style as style
import pandas as pd
import numpy as np

# Set plot style
style.use('ggplot')
style.use('tableau-colorblind10')
style.use('seaborn-v0_8-paper')

# Read the output file
df = pd.read_csv("poisson_burial_1D.csv")

# Convert relevant columns to numeric
columns_to_convert = [
    "Plurality Distortion", "Copeland Distortion", "STV Distortion", 
    "Borda Distortion", "Plurality Veto Distortion"          
]

for col in columns_to_convert:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Ensure 'PSV' is numeric and filter out non-numeric values
df['PSV'] = pd.to_numeric(df['PSV'], errors='coerce')

# Filter the data to include only rows where PSV is numeric and <= 1
df_filtered = df[df['PSV'].notna() & (df['PSV'] <= 1)]

# Define the target value
target_value = 1

# Group by 'PSV' and calculate the percentage of each method choosing the OPT
accuracy_by_psv = df_filtered.groupby('PSV').agg(
    Plurality_percentage=('Plurality Distortion', lambda x: (x == target_value).mean() * 100),
    Copeland_percentage=('Copeland Distortion', lambda x: (x == target_value).mean() * 100),
    STV_percentage=('STV Distortion', lambda x: (x == target_value).mean() * 100),
    Borda_percentage=('Borda Distortion', lambda x: (x == target_value).mean() * 100),
    PluralityVeto_percentage=('Plurality Veto Distortion', lambda x: (x == target_value).mean() * 100)
).reset_index()

# Extract the data
psv_val = accuracy_by_psv["PSV"]

# Create the line plots for each distortion metric
plt.plot(psv_val, accuracy_by_psv["Plurality_percentage"], marker='o', label="Plurality")
plt.plot(psv_val, accuracy_by_psv["Copeland_percentage"], marker='o', label="Copeland")
plt.plot(psv_val, accuracy_by_psv["STV_percentage"], marker='o', label="STV")
plt.plot(psv_val, accuracy_by_psv["Borda_percentage"], marker='o', label="Borda")
plt.plot(psv_val, accuracy_by_psv["PluralityVeto_percentage"], marker='o', label="Plurality Veto")

# Customize the plot
plt.xlabel("Percent of Strategic Voters")
plt.ylabel("Rate of Choosing OPT")
plt.title("Accuracy by Percent of Strategic Voters (n=200, m=5, dist=uniform, strat=compromise, dim=1D)")
plt.xticks(np.arange(0, 1.1, 0.1))  # Set x-axis ticks from 0 to 1 with steps of 0.1
plt.xlim(0, 1)  # Ensure the x-axis ends at 1
plt.ylim(0, 100)  # Set y-axis limits
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')  # Place legend outside the plot
plt.grid(True)  # Add a grid for better readability

# Show the plot
plt.show()