import firebase_admin
from firebase_admin import credentials, db
import pandas as pd
from prophet import Prophet

# Initialize the Firebase app
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://sgm-android-test-default-rtdb.firebaseio.com/'
})

# List of power plant IDs
plant_ids = ['-Nx2n3fX4tZXG6DFHj8O', '-NxXNR6vVdQY2Av4KVWc']

# Initialize lists to store data
data_frames = []

for plant_id in plant_ids:
    # Load historical data
    historical_data = pd.read_csv(f'historical_data_{plant_id}.csv')
    historical_data['date'] = pd.to_datetime(historical_data['date'])
    historical_data.set_index('date', inplace=True)

    # Prepare data for Prophet
    demand_data = historical_data.reset_index()[['date', 'target_capacity']]
    demand_data.columns = ['ds', 'y']

    capacity_data = historical_data.reset_index()[['date', 'total_capacity']]
    capacity_data.columns = ['ds', 'y']

    # Train Prophet model for demand
    demand_model = Prophet()
    demand_model.fit(demand_data)

    # Train Prophet model for capacity
    capacity_model = Prophet()
    capacity_model.fit(capacity_data)

    # Create future dataframe for next 7 days
    future_dates = demand_model.make_future_dataframe(periods=7)
    
    # Make predictions
    demand_forecast = demand_model.predict(future_dates)
    capacity_forecast = capacity_model.predict(future_dates)

    # Save predictions to CSV
    demand_forecast[['ds', 'yhat']].to_csv(f'demand_forecast_{plant_id}.csv', index=False)
    capacity_forecast[['ds', 'yhat']].to_csv(f'capacity_forecast_{plant_id}.csv', index=False)
