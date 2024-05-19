import firebase_admin
from firebase_admin import credentials, db
import pandas as pd
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

try:
    # Initialize the Firebase app
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://sgm-android-test-default-rtdb.firebaseio.com/'
    })

    # List of power plant IDs
    plant_ids = ['-Nx2n3fX4tZXG6DFHj8O', '-NxXNR6vVdQY2Av4KVWc']

    for plant_id in plant_ids:
        # Load predictions
        demand_forecast = pd.read_csv(f'demand_forecast_{plant_id}.csv')
        capacity_forecast = pd.read_csv(f'capacity_forecast_{plant_id}.csv')

        # Convert the 'ds' column to datetime objects
        demand_forecast['ds'] = pd.to_datetime(demand_forecast['ds'])
        capacity_forecast['ds'] = pd.to_datetime(capacity_forecast['ds'])

        # Reference to the data
        ref = db.reference(f'SGM/Prediction/{plant_id}/Date')

        # Update Firebase with predictions
        updates = {}
        for i in range(len(demand_forecast)):
            date = demand_forecast['ds'][i].strftime('%d-%m-%Y')
            updates[f'{date}/capacity/pptargetCapacity'] = demand_forecast['yhat'][i]
            updates[f'{date}/total/pptotalCurrentCapacity'] = capacity_forecast['yhat'][i]

        ref.update(updates)
        logging.info(f"Firebase updated successfully for plant {plant_id}.")

except Exception as e:
    logging.error(f"An error occurred: {e}")