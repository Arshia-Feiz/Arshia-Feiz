import pandas as pd
import matplotlib.pyplot as plt
import pickle
import os
from datetime import datetime
import numpy as np

# Load the half dataset and full dataset
half_data_path = 'DATA_SPY_half.csv'
full_data_path = 'DATA_SPY.csv'

df_half = pd.read_csv(half_data_path, parse_dates=['Date'])
df_full = pd.read_csv(full_data_path, parse_dates=['Date'])

# Load the saved model trained on half of the data
with open('Models/prophet_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Predict from the cutoff point (last date in half dataset) to today
cutoff_date = df_half['Date'].max()
today = datetime.today().strftime('%Y-%m-%d')

# Create a future dataframe from the cutoff date to today
days_to_predict = (pd.to_datetime(today) - cutoff_date).days
future = model.make_future_dataframe(periods=days_to_predict)

# Include the volume regressor for future dates (using average volume)
future['volume'] = df_half['Volume'].mean()
future['floor'] = 1
future['cap'] = df_half['Close'].max() * 1.5  # Use the same cap value as in training

# Make predictions
forecast = model.predict(future)

# Filter the forecast to only include dates from the cutoff date to today
forecast_filtered = forecast[forecast['ds'] > cutoff_date]

# Merge forecast with actual data to ensure matching dates
df_actual = df_full[df_full['Date'] >= cutoff_date]  # Start actual data from cutoff
df_actual = df_actual[['Date', 'Close']].rename(columns={'Date': 'ds', 'Close': 'Actual_Close'})
forecast_filtered = pd.merge(forecast_filtered, df_actual, on='ds', how='left')

# Fill any NaN values in 'Actual_Close' with the previous day's price
forecast_filtered['Actual_Close'].fillna(method='ffill', inplace=True)

# Save the prediction to a CSV file
prediction_file_path = 'SPY_Price_Prediction_Half_to_Today.csv'
forecast_filtered[['ds', 'yhat']].rename(columns={'ds': 'Date', 'yhat': 'Predicted_Close'}).to_csv(prediction_file_path, index=False)

# Plot the prediction vs actual price
plt.figure(figsize=(14, 7))

# Plot the predicted prices
plt.subplot(1, 2, 1)
plt.plot(forecast_filtered['ds'], forecast_filtered['yhat'], label='Predicted Close Price', color='blue')
plt.title('Predicted SPY Price from Half to Today')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()

# Plot the actual prices starting from the cutoff date
plt.subplot(1, 2, 2)
plt.plot(df_actual['ds'], df_actual['Actual_Close'], label='Actual Close Price', color='orange')
plt.title('Actual SPY Price from Half to Today')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()

plt.tight_layout()
plt.show()

# Hypothetical Investment Scenario
initial_fund = 100000  # $100k initial investment
shares_held = 0
cash = initial_fund

# Iterate over the predictions
for i in range(len(forecast_filtered) - 1):
    today_price = forecast_filtered.iloc[i]['yhat']
    tomorrow_price = forecast_filtered.iloc[i + 1]['yhat']
    actual_price_today = forecast_filtered.iloc[i]['Actual_Close']

    if tomorrow_price > today_price:
        # Buy SPY stocks
        shares_held = cash / actual_price_today
        cash = 0
    elif tomorrow_price < today_price:
        # Sell SPY stocks
        cash = shares_held * actual_price_today
        shares_held = 0

# Calculate the final worth
final_actual_price = forecast_filtered['Actual_Close'].iloc[-1]
final_worth = cash + shares_held * final_actual_price

# Calculate the worth if bought and held
buy_and_hold_shares = initial_fund / df_half['Close'].iloc[-1]
buy_and_hold_worth = buy_and_hold_shares * final_actual_price

# Print the results
print(f"Shares held today: {shares_held:.2f}")
print(f"Final portfolio value today: ${final_worth:,.2f}")
print(f"Profit/Loss compared to buy and hold: ${final_worth - buy_and_hold_worth:,.2f}")

print(f"Prediction saved to {prediction_file_path}")
