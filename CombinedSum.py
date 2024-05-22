import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

def initialize_firebase():
    # Fetch the service account key JSON file path
    cred = credentials.Certificate("serviceAccountKey.json")

    # Initialize the app with the service account, granting admin privileges
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://sgm-android-test-default-rtdb.firebaseio.com/'
    })

def get_current_date():
    # Get current date in the specified format
    return datetime.now().strftime("%d-%m-%Y")

# Power Plant Functions
def get_current_capacity_ref(powerplant_id, current_date):
    # Reference to the location in the Firebase database for current capacity
    return db.reference(f"SGM/PowerPlant/{powerplant_id}/Date/{current_date}/capacity/ppcurrentCapacity")

def get_total_capacity_ref(powerplant_id, current_date):
    # Reference to the location in the Firebase database for total current capacity
    return db.reference(f"SGM/PowerPlant/{powerplant_id}/Date/{current_date}/total/pptotalCurrentCapacity")

def get_target_capacity_ref(powerplant_id, current_date):
    # Reference to the location in the Firebase database for target capacity
    return db.reference(f"SGM/PowerPlant/{powerplant_id}/Date/{current_date}/capacity/pptargetCapacity")

def get_all_powerplant_target_capacity_ref(current_date):
    # Reference to the location in the Firebase database for all power plant target capacity
    return db.reference(f"SGM/Date/{current_date}/total/AllpptargetCapacity")

def get_all_powerplant_current_capacity_ref(current_date):
    # Reference to the location in the Firebase database for all power plant current capacity
    return db.reference(f"SGM/Date/{current_date}/total/AllppcurrentCapacity")

def calculate_all_powerplant_capacities(powerplant_ids, current_date):
    # Calculate the total target and current capacities for all power plants
    all_target_capacity = sum([get_target_capacity_ref(pid, current_date).get() or 0 for pid in powerplant_ids])
    all_current_capacity = sum([get_total_capacity_ref(pid, current_date).get() or 0 for pid in powerplant_ids])
    
    all_target_ref = get_all_powerplant_target_capacity_ref(current_date)
    all_current_ref = get_all_powerplant_current_capacity_ref(current_date)
    
    all_target_ref.set(all_target_capacity)
    all_current_ref.set(all_current_capacity)

def update_total_capacity(event, total_capacity_ref, target_capacity_ref, alert_ref, current_capacity_ref, powerplant_ids):
    # Function to update total capacity when current capacity changes
    new_capacity = event.data
    if new_capacity is None:
        new_capacity = 0
    cumulative_sum = total_capacity_ref.get() or 0
    cumulative_sum += new_capacity
    total_capacity_ref.set(cumulative_sum)
    data = current_capacity_ref.get() or 0
    
    # Get target capacity
    target_capacity = target_capacity_ref.get() or 0
    
    # Update alert status
    alert_ref.set(data <= float(target_capacity / 17280))  # Ensure target capacity is treated as numeric
    
    # Update all power plant capacities
    current_date = get_current_date()
    calculate_all_powerplant_capacities(powerplant_ids, current_date)

def monitor_capacity_changes(powerplant_ids):
    # Get current date
    current_date = get_current_date()
    
    # Set up monitoring for each power plant
    for powerplant_id in powerplant_ids:
        # Get references to current, total capacity, target capacity, and alert status for the current power plant
        current_capacity_ref = get_current_capacity_ref(powerplant_id, current_date)
        total_capacity_ref = get_total_capacity_ref(powerplant_id, current_date)
        target_capacity_ref = get_target_capacity_ref(powerplant_id, current_date)
        alert_ref = db.reference(f"SGM/PowerPlant/{powerplant_id}/Date/{current_date}/alert")
        
        # Listen for changes to current capacity for the current power plant
        current_capacity_ref.listen(lambda event, total_capacity_ref=total_capacity_ref, target_capacity_ref=target_capacity_ref, alert_ref=alert_ref, current_capacity_ref=current_capacity_ref: update_total_capacity(event, total_capacity_ref, target_capacity_ref, alert_ref, current_capacity_ref, powerplant_ids))
        
        # Listen for changes to target capacity for the current power plant
        target_capacity_ref.listen(lambda event, powerplant_ids=powerplant_ids: calculate_all_powerplant_capacities(powerplant_ids, current_date))

# Distributor Functions
def get_current_demand_ref(distributor_id, current_date):
    # Reference to the location in the Firebase database for current demand
    return db.reference(f"SGM/Distributor/{distributor_id}/Date/{current_date}/demand/ddcurrentDemand")

def get_total_demand_ref(distributor_id, current_date):
    # Reference to the location in the Firebase database for total current demand
    return db.reference(f"SGM/Distributor/{distributor_id}/Date/{current_date}/total/ddtotalCurrentdemand")

def get_target_demand_ref(distributor_id, current_date):
    # Reference to the location in the Firebase database for target demand
    return db.reference(f"SGM/Distributor/{distributor_id}/Date/{current_date}/demand/ddtargetdemand")

def get_all_distributor_target_demand_ref(current_date):
    # Reference to the location in the Firebase database for all distributor target demand
    return db.reference(f"SGM/Date/{current_date}/total/AllddtargetDemand")

def get_all_distributor_current_demand_ref(current_date):
    # Reference to the location in the Firebase database for all distributor current demand
    return db.reference(f"SGM/Date/{current_date}/total/AllddcurrentDemand")

def calculate_all_distributor_demands(distributor_ids, current_date):
    # Calculate the total target and current demands for all distributors
    all_target_demand = sum([get_target_demand_ref(did, current_date).get() or 0 for did in distributor_ids])
    all_current_demand = sum([get_total_demand_ref(did, current_date).get() or 0 for did in distributor_ids])
    
    all_target_ref = get_all_distributor_target_demand_ref(current_date)
    all_current_ref = get_all_distributor_current_demand_ref(current_date)
    
    all_target_ref.set(all_target_demand)
    all_current_ref.set(all_current_demand)

def update_total_demand(event, total_demand_ref, target_demand_ref, alert_ref, current_demand_ref, distributor_ids):
    # Function to update total demand when current demand changes
    new_demand = event.data
    if new_demand is None:
        new_demand = 0
    cumulative_sum = total_demand_ref.get() or 0
    cumulative_sum += new_demand
    total_demand_ref.set(cumulative_sum)
    data = current_demand_ref.get() or 0

    # Get target demand
    target_demand = target_demand_ref.get() or 0
    
    # Update alert status
    alert_ref.set(data <= float(target_demand / 17280))  # Ensure target demad is treated as numeric
    
    # Update all distributor demands
    current_date = get_current_date()
    calculate_all_distributor_demands(distributor_ids, current_date)

def monitor_demand_changes(distributor_ids):
    # Get current date
    current_date = get_current_date()
    
    # Set up monitoring for each distributor
    for distributor_id in distributor_ids:
        # Get references to current, total demand, and target demand for the current distributor
        current_demand_ref = get_current_demand_ref(distributor_id, current_date)
        total_demand_ref = get_total_demand_ref(distributor_id, current_date)
        target_demand_ref = get_target_demand_ref(distributor_id, current_date)
        alert_ref = db.reference(f"SGM/Distributor/{distributor_id}/Date/{current_date}/alert")

        # Listen for changes to current demand for the current distributor
        current_demand_ref.listen(lambda event, total_demand_ref=total_demand_ref, target_demand_ref=target_demand_ref, alert_ref=alert_ref, current_demand_ref=current_demand_ref: update_total_demand(event, total_demand_ref, target_demand_ref, alert_ref, current_demand_ref, distributor_ids))

        # Listen for changes to target demand for the current distributor
        target_demand_ref.listen(lambda event, distributor_ids=distributor_ids: calculate_all_distributor_demands(distributor_ids, current_date))

if __name__ == "__main__":
    powerplant_ids = ["-NxXNR6vVdQY2Av4KVWc", "-Nx2n3fX4tZXG6DFHj8O"]  # List of power plant IDs
    distributor_ids = [
        "Bangladesh Power Development Board",
        "Dhaka Electric Supply Company Limited",
        "Dhaka Power Distribution Company Limited"
    ] # List of distributor IDs

    # Initialize Firebase
    initialize_firebase()

    # Monitor capacity changes for power plants
    monitor_capacity_changes(powerplant_ids)

    # Monitor demand changes for distributors
    monitor_demand_changes(distributor_ids)

    # Keep the program running
    while True:
        pass
