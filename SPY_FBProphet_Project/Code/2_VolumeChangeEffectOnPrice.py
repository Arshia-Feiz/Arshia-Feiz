import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the data
file_path = 'DATA_SPY.csv'  # Update this path if necessary
df = pd.read_csv(file_path, parse_dates=['Date'])

# Calculate daily price change from open to close
df['Price_Change'] = df['Close'] - df['Open']

# Calculate percentage change in volume
df['Volume_Change_%'] = df['Volume'].pct_change() * 100

# Calculate average daily volume
average_volume = df['Volume'].mean()

# Classify days based on whether the price increased or decreased
df['Price_Direction'] = np.where(df['Price_Change'] > 0, 'Increase', 'Decrease')

# Calculate the percentage of days where volume increase led to a price increase or decrease
df['Volume_Increase'] = df['Volume_Change_%'] > 0

# Filter out rows with no volume change
df_nonzero_volume = df[df['Volume_Change_%'] != 0]

# Calculate the number of times volume increase led to price increase and decrease
volume_increase_price_increase = df_nonzero_volume[(df_nonzero_volume['Volume_Increase']) & (df_nonzero_volume['Price_Change'] > 0)].shape[0]
volume_increase_price_decrease = df_nonzero_volume[(df_nonzero_volume['Volume_Increase']) & (df_nonzero_volume['Price_Change'] < 0)].shape[0]

# Calculate the percentage of these events
total_volume_increases = df_nonzero_volume['Volume_Increase'].sum()
percentage_price_increase = (volume_increase_price_increase / total_volume_increases) * 100
percentage_price_decrease = (volume_increase_price_decrease / total_volume_increases) * 100

# Create a summary table
summary_data = {
    "Metric": ["Average Daily Volume", "Volume Increase Resulting in Price Increase", "Volume Increase Resulting in Price Decrease"],
    "Value": [f"${average_volume:,.0f}", f"{percentage_price_increase:.2f}%", f"{percentage_price_decrease:.2f}%"]
}
summary_df = pd.DataFrame(summary_data)

# Display the summary table using print
print(summary_df)

# Plotting the summary statistics
plt.figure(figsize=(14, 7))

# Bar chart for percentage increases and decreases
plt.subplot(1, 2, 1)
sns.barplot(x=["Price Increase", "Price Decrease"], y=[percentage_price_increase, percentage_price_decrease], palette='coolwarm')

# Adding labels to the bars
for i, value in enumerate([percentage_price_increase, percentage_price_decrease]):
    plt.text(i, value + 0.5, f'{value:.2f}%', ha='center', va='bottom', fontsize=12)

plt.title('Effect of Volume Increase on Price Direction', fontsize=14, fontweight='bold')
plt.ylabel('Percentage (%)', fontsize=12)

# Plot of average daily volume
plt.subplot(1, 2, 2)
plt.bar(["Average Daily Volume"], [average_volume], color='dodgerblue')

# Adding label to the bar with $ sign
plt.text(0, average_volume + average_volume * 0.01, f'${average_volume:,.0f}', ha='center', va='bottom', fontsize=12)

plt.title('Average Daily Volume', fontsize=14, fontweight='bold')
plt.ylabel('Volume', fontsize=12)

plt.tight_layout()
plt.show()
