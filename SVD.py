import matplotlib.pyplot as plt
import matplotlib.style as style
import pandas as pd
import numpy as np

# Set plot style
style.use('ggplot')
style.use('tableau-colorblind10')
style.use('seaborn-v0_8-paper')

# Read the output file
df = pd.read_csv("uniform_compromise_1D.csv")

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

# Group by 'PSV' and calculate the average distortion for each method
distortion_by_psv = df_filtered.groupby('PSV').agg(
    Plurality_distortion=('Plurality Distortion', 'mean'),
    Copeland_distortion=('Copeland Distortion', 'mean'),
    STV_distortion=('STV Distortion', 'mean'),
    Borda_distortion=('Borda Distortion', 'mean'),
    PluralityVeto_distortion=('Plurality Veto Distortion', 'mean')
).reset_index()

# Extract the data
psv_val = distortion_by_psv["PSV"]

# Create the line plots for each distortion metric
plt.figure(figsize=(10, 6))
plt.plot(psv_val, distortion_by_psv["Plurality_distortion"], marker='o', label="Plurality")
plt.plot(psv_val, distortion_by_psv["Copeland_distortion"], marker='o', label="Copeland")
plt.plot(psv_val, distortion_by_psv["STV_distortion"], marker='o', label="STV")
plt.plot(psv_val, distortion_by_psv["Borda_distortion"], marker='o', label="Borda")
plt.plot(psv_val, distortion_by_psv["PluralityVeto_distortion"], marker='o', label="Plurality Veto")

# Customize the plot
plt.xlabel("Percent of Strategic Voters")
plt.ylabel("Average Distortion")
plt.title("Distortion by Percent of Strategic Voters (n=200, m=5, dist=uniform, strat=compromise, dim=1D)")
plt.xticks(np.arange(0, 1.1, 0.1))  # Set x-axis ticks from 0 to 1 with steps of 0.1
plt.xlim(0, 1)  # Ensure the x-axis ends at 1
plt.ylim(bottom=1)  # Distortion cannot be less than 1
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')  # Place legend outside the plot
plt.grid(True)  # Add a grid for better readability

# Show the plot
plt.tight_layout()
plt.show()