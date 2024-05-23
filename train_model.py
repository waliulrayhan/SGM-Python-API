import firebase_admin
from firebase_admin import credentials, db
import pandas as pd
from prophet import Prophet
import numpy as np
from datetime import datetime

def initialize_firebase():
    # Initialize the Firebase app
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://sgm-android-test-default-rtdb.firebaseio.com/'
    })

def load_historical_data(plant_id):
    # Load historical data
    historical_data = pd.read_csv(f'history_data_{plant_id}.csv')
    historical_data['date'] = pd.to_datetime(historical_data['date'])
    historical_data.set_index('date', inplace=True)
    return historical_data

def prepare_data_for_prophet(historical_data):
    # Prepare data for Prophet
    demand_data = historical_data.reset_index()[['date', 'target_capacity']]
    demand_data.columns = ['ds', 'y']
    capacity_data = historical_data.reset_index()[['date', 'total_capacity']]
    capacity_data.columns = ['ds', 'y']
    return demand_data, capacity_data

def train_prophet_model(data):
    # Train Prophet model
    model = Prophet()
    model.fit(data)
    return model

def make_predictions(model):
    # Get the current date
    today = datetime.now().date()
    # Create future dataframe for the next 7 days
    future_dates = model.make_future_dataframe(periods=7)
    # Filter out past and current dates, keep only future dates
    future_dates = future_dates[future_dates['ds'] > pd.to_datetime(today)]
    forecast = model.predict(future_dates)
    return forecast

def apply_capacity_constraint(demand_forecast, capacity_forecast):
    # Ensure total_capacity <= target_capacity with some variability
    constrained_capacity = capacity_forecast[['ds', 'yhat']].copy()
    constrained_capacity['yhat'] = constrained_capacity.apply(
        lambda row: min(row['yhat'], 
                        demand_forecast.loc[demand_forecast['ds'] == row['ds'], 'yhat'].values[0] * np.random.uniform(0.95, 1.0)), 
        axis=1)
    return constrained_capacity

def save_predictions(plant_id, demand_forecast, capacity_forecast):
    # Save predictions to CSV
    demand_forecast[['ds', 'yhat']].to_csv(f'demand_forecast_{plant_id}.csv', index=False)
    capacity_forecast[['ds', 'yhat']].to_csv(f'capacity_forecast_{plant_id}.csv', index=False)

def main():
    # List of power plant IDs
    plant_ids = ['-Nx2n3fX4tZXG6DFHj8O', '-NxXNR6vVdQY2Av4KVWc', '-Nya8gUllGemye6qSYcs']

    # Initialize Firebase
    initialize_firebase()

    for plant_id in plant_ids:
        # Load and prepare historical data
        historical_data = load_historical_data(plant_id)
        demand_data, capacity_data = prepare_data_for_prophet(historical_data)

        # Train Prophet models
        demand_model = train_prophet_model(demand_data)
        capacity_model = train_prophet_model(capacity_data)

        # Make predictions
        demand_forecast = make_predictions(demand_model)
        capacity_forecast = make_predictions(capacity_model)

        # Apply capacity constraint with variability
        constrained_capacity_forecast = apply_capacity_constraint(demand_forecast, capacity_forecast)

        # Save predictions to CSV
        save_predictions(plant_id, demand_forecast, constrained_capacity_forecast)

if __name__ == "__main__":
    main()
