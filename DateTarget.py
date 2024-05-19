import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

# Initialize Firebase Admin SDK
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://sgm-android-test-default-rtdb.firebaseio.com/'
})

# Get current date
current_date = datetime.now().strftime("%d-%m-%Y")

# Upload data to Firebase
def upload_data_to_firebase():
    ref = db.reference('SGM')

    # PowerPlant data
    power_plant_ref = ref.child('PowerPlant')
    for snapshot in power_plant_ref.get().items():
        power_plant_key = snapshot[0]
        power_plant_date_ref = power_plant_ref.child(power_plant_key).child('Date').child(current_date)
        power_plant_date_ref.child('capacity').child('ppcurrentCapacity').set(0)
        power_plant_date_ref.child('capacity').child('pptargetCapacity').set(0)
        power_plant_date_ref.child('total').child('pptotalCurrentCapacity').set(0)
        power_plant_date_ref.child('alert').set(False)
        power_plant_date_ref.child('history').child('pptotalCurrentCapacity').set(0)
        power_plant_date_ref.child('history').child('last_update_time').set('11.59.59 PM')

    # Distributor data
    distributor_ref = ref.child('Distributor')
    for snapshot in distributor_ref.get().items():
        distributor_key = snapshot[0]
        distributor_date_ref = distributor_ref.child(distributor_key).child('Date').child(current_date)
        distributor_date_ref.child('demand').child('ddcurrentDemand').set(0)
        distributor_date_ref.child('demand').child('ddtargetdemand').set(0)
        distributor_date_ref.child('total').child('ddtotalCurrentdemand').set(0)
        distributor_date_ref.child('alert').set(False)
        distributor_date_ref.child('history').child('ddtotalCurrentDemand').set(0)
        distributor_date_ref.child('history').child('last_update_time').set('11.59.59 PM')

    # Date data
    date_ref = ref.child('Date').child(current_date).child('total')
    date_ref.child('AllppcurrentCapacity').set(0)
    date_ref.child('AllpptargetCapacity').set(0)
    date_ref.child('AllddcurrentDemand').set(0)
    date_ref.child('AllddtargetDemand').set(0)

# Call the function to upload data
upload_data_to_firebase()
