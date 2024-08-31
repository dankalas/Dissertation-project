import math
import random
import pandas as pd
import requests
import numpy as np
from gplearn.genetic import SymbolicRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt


# Define your Mapbox token
MAPBOX_TOKEN = 'pk.eyJ1IjoiZGFuaWVsYWthbGFtdWRvIiwiYSI6ImNseW4wNno4bTAxNDAya3M0YjJqNHkwamMifQ.RXniMT8_Seus5fdPUJ2XRA'

# Average speeds in km/h for different modes
speeds = {
    "driving": 60,
    "traffic": 50,
    "walking": 5,
    "cycling": 15
}

# Calories burned per hour
calories_burned_per_hour = {
    "driving": 0,
    "traffic": 0,
    "walking": 300,
    "cycling": 600
}

# Carbon footprint in grams of CO2 per kilometer
carbon_footprint_per_km = {
    "driving": 170,
    "traffic": 150,
    "walking": 0,
    "cycling": 0
}

# Function to get coordinates from location names
def geocode_location(location):
    url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{location}.json?access_token={MAPBOX_TOKEN}"
    response = requests.get(url)
    data = response.json()
    
    if len(data['features']) == 0:
        print(f"Location '{location}' not found. Please check the spelling or try a more specific location.")
        return None

    return data['features'][0]['center']

def get_routes(start_coords, end_coords, mode):
    # Validate mode input to ensure it's one of the accepted modes by Mapbox
    valid_modes = ['driving', 'walking', 'cycling','traffic']
    if mode not in valid_modes:
        raise ValueError(f"Invalid mode. Choose from {valid_modes}")

    # Construct the URL with the selected mode
    url = f"https://api.mapbox.com/directions/v5/mapbox/{mode}/{start_coords[0]},{start_coords[1]};{end_coords[0]},{end_coords[1]}?geometries=geojson&alternatives=true&access_token={MAPBOX_TOKEN}"
    
    # Send the request to Mapbox API
    response = requests.get(url)
    
    # Handle potential errors from the API response
    if response.status_code != 200:
        raise Exception(f"Mapbox API error: {response.status_code}, {response.text}")
    
    # Extract routes from the response
    routes = response.json().get('routes', [])
    
    return routes
# Function to process routes into a dataframe
def process_routes(routes):
    data = []
    for idx, route in enumerate(routes):
        data.append({
            'Route Label': f'Route {idx + 1}',
            'Distance (km)': route['distance'] / 1000,  # Convert to kilometers
            'Duration (minutes)': route['duration'] / 60,  # Convert to minutes
        })
    return pd.DataFrame(data)

# Function to apply custom weights and calculate the weighted score
def apply_weights(df, weights):
    required_columns = [
        "Norm Time", "Norm Distance", "Norm Calories",
        "Norm Carbon", "Norm Noise", "Norm Scenic",
        "Norm AQI", "Norm Safety Rating"
    ]
    
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    # Calculate the weighted score
    df["Weighted Score"] = (
        weights["Norm Time"] * df["Norm Time"] +
        weights["Norm Distance"] * df["Norm Distance"] +
        weights["Norm Calories"] * df["Norm Calories"] +
        weights["Norm Carbon"] * df["Norm Carbon"] +
        weights["Norm Noise"] * df["Norm Noise"] +
        weights["Norm Scenic"] * df["Norm Scenic"] +
        weights["Norm AQI"] * df["Norm AQI"] +
        weights["Norm Safety Rating"] * df["Norm Safety Rating"]
    )
    
    return df

# Function to generate additional data for symbolic regression
def generate_additional_data(df, mode):
    data = {
        "Distance (km)": [],
        "Time (minutes)": [],
        "Calories Burned": [],
        "Carbon Footprint (g CO2)": [],
        "Noise Pollution (dB)": [],
        "Scenic Score": [],
        "AQI": [],
        "Safety Rating": [],
        "Time Interval": [],
        "Route Label": []
    }
    
    speed = speeds[mode]
    for _, row in df.iterrows():
        # Add "Today" data
        data["Distance (km)"].append(row['Distance (km)'])
        data["Time (minutes)"].append(row['Duration (minutes)'])
        time_hours = row['Distance (km)'] / speed
        data["Calories Burned"].append(round(calories_burned_per_hour[mode] * time_hours))
        data["Carbon Footprint (g CO2)"].append(round(carbon_footprint_per_km[mode] * row['Distance (km)']))
        data["Noise Pollution (dB)"].append(random.randint(20, 70))
        data["Scenic Score"].append(random.randint(1, 10))
        base_aqi = random.randint(10, 60)
        aqi_variation = random.uniform(-0.1, 0.1)
        data["AQI"].append(round(base_aqi * (1 + aqi_variation)))
        data["Safety Rating"].append(random.randint(1, 5))
        data["Time Interval"].append("Today")
        data["Route Label"].append(row['Route Label'])
        
        # Generate data for historical intervals
        for time_interval in ["A Week ago", "Two Weeks Ago", "Three Weeks Ago"]:
            # Introduce slight variations in distance (up to ±5%)
            distance_variation = random.uniform(-0.05, 0.05)
            distance = row['Distance (km)'] * (1 + distance_variation)

            # Recalculate time in minutes based on varied distance
            time_hours = distance / speed
            time_minutes = round(time_hours * 60)

            # Calculate calories burned (rounded to nearest whole number)
            calories_burned = round(calories_burned_per_hour[mode] * time_hours)

            # Calculate carbon footprint (rounded to nearest whole number)
            carbon_footprint = round(carbon_footprint_per_km[mode] * distance)

            # Generate random values for noise pollution, AQI, and safety rating
            noise_pollution = random.randint(20, 70)

            # Introduce slight variations in AQI (up to ±10%)
            aqi_variation = random.uniform(-0.1, 0.1)
            base_aqi = random.randint(10, 60)
            aqi = round(base_aqi * (1 + aqi_variation))

            data["Distance (km)"].append(distance)
            data["Time (minutes)"].append(time_minutes)
            data["Calories Burned"].append(calories_burned)
            data["Carbon Footprint (g CO2)"].append(carbon_footprint)
            data["Noise Pollution (dB)"].append(noise_pollution)
            data["Scenic Score"].append(random.randint(1, 10))
            data["AQI"].append(aqi)
            data["Safety Rating"].append(random.randint(1, 5))
            data["Time Interval"].append(time_interval)
            data["Route Label"].append(row['Route Label'])

    return pd.DataFrame(data)

# Function to normalize data
def normalize(value, min_value, max_value):
    return (value - min_value) / (max_value - min_value)

# Function to get weights from user input
def get_user_weights():
    weights = {}
    print("Enter weights for each parameter (default is 1 if left blank):")
    
    weights["Norm Time"] = float(input("Weight for Time: ") or 1)
    weights["Norm Distance"] = float(input("Weight for Distance: ") or 1)
    weights["Norm Calories"] = float(input("Weight for Calories: ") or 1)
    weights["Norm Carbon"] = float(input("Weight for Carbon: ") or 1)
    weights["Norm Noise"] = float(input("Weight for Noise: ") or 1)
    weights["Norm Scenic"] = float(input("Weight for Scenic: ") or 1)
    weights["Norm AQI"] = float(input("Weight for AQI: ") or 1)
    weights["Norm Safety Rating"] = float(input("Weight for Accident Rate: ") or 1)
    
    return weights


def run_process(start_location, end_location, mode, weights):
    
    # Get coordinates
    start_coords = geocode_location(start_location)
    end_coords = geocode_location(end_location)
    
    if start_coords is None or end_coords is None:
        print("Unable to retrieve coordinates for the provided locations.")
        return
    
    # Get routes
    routes = get_routes(start_coords, end_coords, mode)
    
    # Process routes into a dataframe
    df = process_routes(routes)
    
    # Generate additional data based on the selected mode
    additional_data_df = generate_additional_data(df, mode)
    
    # Normalize the data
    df2 = additional_data_df
    df2["Norm Distance"] = normalize(df2["Distance (km)"], 0, 200)
    df2["Norm Time"] = normalize(df2["Time (minutes)"], 0, 1200)
    df2["Norm Calories"] = normalize(df2["Calories Burned"], 0, 5500)
    df2["Norm Carbon"] = normalize(df2["Carbon Footprint (g CO2)"], 0, 30000)
    df2["Norm Noise"] = normalize(df2["Noise Pollution (dB)"], 0, 100)
    df2["Norm Scenic"] = normalize(df2["Scenic Score"], 1, 10)
    df2["Norm AQI"] = normalize(df2["AQI"], 0, 70)
    df2["Norm Safety Rating"] = normalize(df2["Safety Rating"], 0, 5)


    
    # Create separate dataframes for each route label
    route_labels = df2["Route Label"].unique()
    route_dfs = {}
    for label in route_labels:
        route_dfs[label] = df2[df2["Route Label"] == label].copy().reset_index(drop=True)
    
    # Create a dictionary to store X, y, and the first row of each route
    route_data = {}

    # Loop through each route label and process the data
    for label, route_df in route_dfs.items():
        if route_df is not None:
            # Apply weights to the current route dataframe
            route_df_weighted = apply_weights(route_df, weights)
            print(f"Weighted Data for {label}:")
            print(route_df_weighted)
            
            # Extract X and y for the current route
            X = route_df_weighted[[
                "Time (minutes)", "Distance (km)", "Calories Burned", 
                "Carbon Footprint (g CO2)", "Noise Pollution (dB)", 
                "Scenic Score", "AQI", "Safety Rating"
            ]]
            y = route_df_weighted["Weighted Score"]
            
            # Store X, y, and the first row of the route dataframe
            route_data[label] = {
                'X': X,
                'y': y,
                'first_row': route_df.iloc[0]  # Store the first row of the route dataframe
            }

    # Dictionary to store RMSE values for each route
    route_rmse = {}

    # Define the function to fit the symbolic regression model
    def fit_symbolic_regression(X, y):
        est = SymbolicRegressor(
            population_size=5000,
            generations=20, 
            stopping_criteria=0.01,
            p_crossover=0.7, 
            p_subtree_mutation=0.1,
            p_hoist_mutation=0.05, 
            p_point_mutation=0.1,
            max_samples=0.9, 
            verbose=1,
            parsimony_coefficient=0.01, 
            random_state=0
        )
        est.fit(X, y)
        return est

    # Track RMSE and the first row for each route
    route_results = []

    # Train and evaluate a symbolic regression model for each route
    for label, data in route_data.items():
        X = data['X']
        y = data['y']
        
        # Initialize and train the symbolic regression model
        model = fit_symbolic_regression(X, y)
        
        # Make predictions
        y_pred = model.predict(X)
        
        # Calculate RMSE
        rmse = np.sqrt(mean_squared_error(y, y_pred))
        route_rmse[label] = rmse
        
        # Get the first row from the stored data
        first_row = data['first_row']
        
        # Append route, RMSE, and the first row to the results list
        route_results.append({
            'Route Label': label,
            'RMSE': rmse,
            'First Row': first_row
        })
        
        print(f"Route: {label}")
        print(f"RMSE: {rmse}")

    # Sort results by RMSE (lowest first)
    route_results.sort(key=lambda x: x['RMSE'])
    
    # Display RMSE results
    print("RMSE for each route:")
    for result in route_results:
        print(f"Route {result['Route Label']}: RMSE = {result['RMSE']}")

    # Return the ranked routes with RMSE and the first row of each route
    return route_results

