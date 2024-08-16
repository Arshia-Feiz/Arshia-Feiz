import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mplfinance as mpf

# Load the data
file_path = 'DATA_SPY.csv'  # Update this path if necessary
df = pd.read_csv(file_path, parse_dates=['Date'])

# Display the first few rows of the dataframe
print("First 5 rows of the dataset:")
print(df.head())

# Basic statistics
print("\nBasic Statistics:")
print(df.describe())

# Check for missing values
print("\nMissing values:")
print(df.isnull().sum())

# Set the overall aesthetic style for the plots
sns.set(style='whitegrid')

# Plotting
plt.figure(figsize=(16, 10))

# 1. Line plot of the closing price over time
plt.subplot(2, 2, 1)
plt.plot(df['Date'], df['Close'], color='dodgerblue', label='Close Price', linewidth=1.5)
plt.title('Closing Price Over Time', fontsize=14, fontweight='bold')
plt.xlabel('Date', fontsize=12)
plt.ylabel('Close Price', fontsize=12)
plt.xticks(rotation=45)
plt.legend()

# 2. Volume traded over time
plt.subplot(2, 2, 2)
plt.plot(df['Date'], df['Volume'], color='darkorange', label='Volume Traded', linewidth=1.5)
plt.title('Volume Traded Over Time', fontsize=14, fontweight='bold')
plt.xlabel('Date', fontsize=12)
plt.ylabel('Volume', fontsize=12)
plt.xticks(rotation=45)
plt.legend()

# 3. Distribution of returns (percentage change in the closing price)
df['Returns'] = df['Close'].pct_change()

plt.subplot(2, 2, 3)
sns.histplot(df['Returns'].dropna(), kde=True, bins=50, color='purple')
plt.title('Distribution of Returns', fontsize=14, fontweight='bold')
plt.xlabel('Daily Returns', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.grid(True)

# 4. Correlation heatmap
plt.subplot(2, 2, 4)
sns.heatmap(df.corr(), annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5, square=True, cbar_kws={"shrink": .75})
plt.title('Correlation Heatmap', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.show()
