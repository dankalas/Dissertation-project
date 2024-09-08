from flask import Flask, request, jsonify, Blueprint
from flask_login import current_user
from .models import Route, Navigation
from .route_optimizer import run_process  # Ensure this matches the filename where run_process is located
from . import db

optimizer = Blueprint('optimizer', __name__)

# Route to optimize the route and save it to the database
@optimizer.route('/optimize_route', methods=['POST'])
def optimize_route():
    data = request.json
    start_location = data['start_location']
    end_location = data['end_location']
    mode = data['mode']
    weights = data['weights']
    
    # Create and save Navigation instance
    nav = Navigation(
        start_location=data["start_location_name"],
        end_location=data["end_location_name"],
        mode=data["mode"],
        user_id=current_user.id
    )
    db.session.add(nav)
    db.session.commit()  # Commit now to generate the navigation ID

    # Call the run_process function and get the optimized routes
    optimized_routes = run_process(start_location, end_location, mode, weights)
    print(optimized_routes)

    # Save the optimized routes in the database
    route_models = list(map(lambda route: Route(
        navigation_id=nav.id,
        aqi_value=route['AQI'],
        distance=route['Distance (km)'],
        calories=route['Calories Burned'],
        carbon_emissions=route['Carbon Footprint (g CO2)'],
        noise_pollution=route['Noise Pollution (dB)'],
        safety_score=route['Safety Rating'],
        scenic_score=route['Scenic Score'],
        time=route['Time (minutes)'],
        route_label=route['Route Label'],
        rmse=route['RMSE']
    ), optimized_routes))
    
    db.session.add_all(route_models)
    db.session.commit()

    # Return the routes label, first index of the route and their RMSE values
    return jsonify({
        'success': True,
        'optimized_routes': optimized_routes,
        'navigation_id': nav.id
    })


