import pandas as pd

# Load the original CSV file
file_path = 'DATA_SPY.csv'  # Update this path if necessary
df = pd.read_csv(file_path, parse_dates=['Date'])

# Determine the midpoint year
midpoint_year = df['Date'].dt.year.median()

# Filter the dataframe to include only rows until the midpoint year
df_half = df[df['Date'].dt.year <= midpoint_year]

# Save the filtered dataframe to a new CSV file
df_half.to_csv('DATA_SPY_half.csv', index=False)

print(f"New CSV file with data until {int(midpoint_year)} created: 'DATA_SPY_half.csv'")



# Load the original CSV file
file_path = 'DATA_SPY.csv'  # Update this path if necessary
df = pd.read_csv(file_path, parse_dates=['Date'])

# Determine the year that corresponds to 80% of the data
percentile_80_year = df['Date'].dt.year.quantile(0.8)

# Filter the dataframe to include only rows until the 80% year
df_80 = df[df['Date'].dt.year <= percentile_80_year]

# Save the filtered dataframe to a new CSV file
df_80.to_csv('DATA_SPY_80.csv', index=False)

print(f"New CSV file with data until approximately {int(percentile_80_year)} created: 'DATA_SPY_80.csv'")

