import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from prophet import Prophet
from prophet.diagnostics import cross_validation, performance_metrics
import pickle
import os

# Load the 80% dataset
file_path = 'DATA_SPY_80.csv'  # Make sure the file path is correct
df = pd.read_csv(file_path, parse_dates=['Date'])

# Prepare the data for Prophet
df_prophet = df[['Date', 'Close']].rename(columns={'Date': 'ds', 'Close': 'y'})

# Define US holidays manually
us_holidays = pd.DataFrame({
    'holiday': 'us_holiday',
    'ds': pd.to_datetime([
        '2022-01-01', '2022-12-25', '2023-01-01', '2023-12-25',  # Add more holidays as needed
    ]),
    'lower_window': 0,
    'upper_window': 1,
})

# Adding volume as a regressor
df_prophet['volume'] = df['Volume']

# Ensure that no price is below zero by applying a floor
df_prophet['floor'] = 1  # Set floor at 1 to prevent going to zero
df_prophet['cap'] = df_prophet['y'].max() * 1.5  # Setting a reasonable cap

# Create the Prophet model
model = Prophet(
    daily_seasonality=True,
    yearly_seasonality=True,
    weekly_seasonality=True,
    holidays=us_holidays,
    seasonality_mode='multiplicative',
    growth='logistic'
)

# Add the volume as a regressor
model.add_regressor('volume')

# Fit the model
model.fit(df_prophet)

# Save the model to the Models folder for future use
os.makedirs('Models', exist_ok=True)
with open('Models/prophet_model_80.pkl', 'wb') as f:
    pickle.dump(model, f)

# Create a dataframe for future predictions
future = model.make_future_dataframe(periods=365)

# Include the volume regressor for future dates
future['volume'] = df_prophet['volume'].mean()  # Assuming average volume for simplicity
future['floor'] = 1
future['cap'] = df_prophet['cap'].iloc[0]  # Use the same cap value

# Predict the future
forecast = model.predict(future)

# Plot the forecast
fig = model.plot(forecast)
plt.title('SPY Price Forecast Using 80% Data')
plt.show()

# Plot forecast components
fig2 = model.plot_components(forecast)
plt.show()

# Perform cross-validation to evaluate the model
df_cv = cross_validation(model, initial='730 days', period='180 days', horizon='365 days')

# Compute performance metrics
df_p = performance_metrics(df_cv)
print(df_p.head())
