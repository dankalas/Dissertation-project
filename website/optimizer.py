from flask import Flask, request, jsonify, Blueprint
from flask_login import current_user
from .models import Route, Navigation
from .route_optimizer import run_process  # Ensure this matches the filename where run_process is located
from . import db
from .summary_utilis import calculate_weekly_summary_task  # Import the Celery task for weekly summary

# Create a Blueprint for the optimizer routes
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
        start_location=start_location,
        end_location=end_location,
        mode=mode,
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


# Route to complete a journey and calculate weekly summary
@optimizer.route('/complete_journey', methods=['POST'])
def complete_journey():
    data = request.get_json()

    user_id = data.get('user_id', current_user.id)  # Use current_user if no user_id is provided
    start_location = data['start_location']
    end_location = data['end_location']
    mode = data['mode']

    # Create a new Navigation entry
    navigation = Navigation(
        user_id=user_id,
        start_location=start_location,
        end_location=end_location,
        mode=mode,
    )
    db.session.add(navigation)
    db.session.commit()

    # Add the Route data
    route = Route(
        navigation_id=navigation.id,
        time=data['time'],
        distance=data['distance'],
        calories=data['calories'],
        carbon_emissions=data['carbon_emissions'],
        noise_pollution=data['noise_pollution'],
        scenic_score=data['scenic_score'],
        aqi_value=data['aqi_value'],
        safety_score=data['safety_score'],
        route_label=data['route_label'],
        rmse=data['rmse'],
    )
    db.session.add(route)
    db.session.commit()

    # Trigger the Celery task asynchronously to calculate weekly summary
    calculate_weekly_summary_task.delay(user_id)

    return {"message": "Journey completed and weekly summary will be updated!"}, 200

@optimizer.route('/api/metrics', methods=['GET'])
def get_metrics():
    user_id = current_user.id  # or get it from query params if needed

    # Fetch weekly summary for the current user
    current_date = datetime.now(ZoneInfo("UTC"))
    start_of_week = current_date - timedelta(days=current_date.weekday())

    # Query the database for the weekly summary
    weekly_summary = WeeklySummary.query.filter_by(user_id=user_id, week_start=start_of_week).first()

    if not weekly_summary:
        return jsonify({'error': 'No metrics found for this week.'}), 404

    return jsonify({
        'total_carbon_emissions': weekly_summary.total_carbon_emissions,
        'total_calories_burned': weekly_summary.total_calories_burned,
        'carbon_diff': weekly_summary.carbon_diff,
        'calories_diff': weekly_summary.calories_diff
    })
