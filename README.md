<h1 align="center">SGM Python API - Smart Grid Management System</h1>

[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

This repository contains the Python API for the **Smart Grid Management System** that uses Firebase for real-time power plant and distributor data storage and management. It integrates IoT sensors to track energy production, demand, and capacity for power plants and distributors. Additionally, the API includes forecasting capabilities to predict future energy needs using historical data.

## Overview

This API manages the **Smart Grid** infrastructure, providing the following functionalities:
- **Power Plant Management**: Monitoring current and target capacities, updating total capacities, and sending alerts based on capacity thresholds.
- **Distributor Management**: Monitoring current and target demand, calculating and updating total demand.
- **Real-time Monitoring**: Using Firebase to capture live data from power plants and distributors.
- **Historical Data Extraction**: Saving historical data for further analysis and forecasting.
- **Forecasting with Prophet**: Predicting future power demand and capacities using machine learning (Prophet).
- **Firebase Integration**: All data is stored and monitored through Firebase Real-time Database.

## Features

- **Real-Time Data**: Continuously monitors power plants' and distributors' energy status (capacity/demand).
- **Capacity & Demand Forecasting**: Predicts future energy requirements and adjusts grid operations accordingly.
- **Alert System**: Notifies if capacity or demand falls below target thresholds.
- **Historical Data Export**: Extracts historical energy data and exports it as CSV files.
- **Firebase Integration**: Real-time database connection for energy data tracking and management.

## Installation

### Prerequisites

- **Python 3.8+**
- **Firebase Admin SDK**
- **Pandas**
- **Prophet** for forecasting (Facebook Prophet)
- **Firebase Project** with Real-time Database set up

### Steps to Install

1. Clone this repository:
    ```bash
    git clone https://github.com/waliulrayhan/SGM-Python-API.git
    cd SGM-Python-API
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up your Firebase project:
    - Download your Firebase service account key (JSON format) and place it in the root directory as `serviceAccountKey.json`.
    - Ensure your Firebase Realtime Database URL is properly configured in the code.

4. Run the application:
    ```bash
    python app.py
    ```

## Usage

### Power Plant & Distributor Monitoring

The API provides functions to monitor power plants and distributors in real-time. The following functions allow you to manage capacities and demands:

- `monitor_capacity_changes(powerplant_ids)`: Monitors changes in power plants’ capacities.
- `monitor_demand_changes(distributor_ids)`: Monitors changes in distributors’ demands.

### Forecasting with Prophet

You can train forecasting models using historical data and Prophet:

- `train_prophet_model(data)`: Trains a model using historical capacity or demand data.
- `make_predictions(model)`: Predicts future values based on the trained model.

### Firebase Data

All real-time and historical data are stored in the Firebase Realtime Database under the following structure:
```plaintext
SGM
 ├── PowerPlant
 │    └── <powerplant_id>
 │        └── Date
 │            └── <date>
 │                ├── capacity
 │                ├── total
 │                └── alert
 ├── Distributor
 │    └── <distributor_id>
 │        └── Date
 │            ├── demand
 │            ├── total
 │            └── alert
 └── Date
      └── <date>
```

### Example Code
```bash
# Initialize Firebase
initialize_firebase()

# Monitor power plants and distributors
powerplant_ids = ["plant1", "plant2"]
distributor_ids = ["distributor1", "distributor2"]

monitor_capacity_changes(powerplant_ids)
monitor_demand_changes(distributor_ids)
```

### Historical Data Extraction
You can extract historical data from Firebase to analyze or use in forecasting:
```bash
extract_historical_data(plant_id)
```

### Forecasting Example
Train models and make predictions for the next 7 days:
```bash
historical_data = load_historical_data(plant_id)
demand_data, capacity_data = prepare_data_for_prophet(historical_data)
demand_model = train_prophet_model(demand_data)
capacity_model = train_prophet_model(capacity_data)
demand_forecast = make_predictions(demand_model)
capacity_forecast = make_predictions(capacity_model)

```

## Contribution

Feel free to open an issue or submit a pull request for any feature requests, bug fixes, or improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

If you have any questions, feel free to contact the project team:

- **Md. Waliul Islam Rayhan**: [LinkedIn](https://www.linkedin.com/in/waliulrayhan)
