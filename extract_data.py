import firebase_admin
from firebase_admin import credentials, db
import pandas as pd

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
    # Reference to the data for each power plant
    ref = db.reference(f'SGM/PowerPlant/{plant_id}/Date')
    data = ref.get()
    
    if data:
        dates = []
        target_capacities = []
        total_capacities = []

        for date, values in data.items():
            dates.append(date)
            target_capacities.append(values['capacity']['pptargetCapacity'])
            total_capacities.append(values['total']['pptotalCurrentCapacity'])

        df = pd.DataFrame({'date': dates, 'target_capacity': target_capacities, 'total_capacity': total_capacities})
        df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
        df.set_index('date', inplace=True)
        df['plant_id'] = plant_id  # Add plant_id column to distinguish data from different plants

        # Save each DataFrame to a separate CSV file
        df.to_csv(f'history_data_{plant_id}.csv')
        data_frames.append(df)

# Concatenate all DataFrames
final_df = pd.concat(data_frames)

# Save the combined DataFrame to a CSV file
final_df.to_csv('history_data_combined.csv')
