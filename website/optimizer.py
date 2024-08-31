# app.py
from flask import Flask, request, jsonify, Blueprint
from  .route_optimizer import run_process  # Ensure this matches the filename where run_process is located

optimizer =  Blueprint('optimizer', __name__)

@optimizer.route('/optimize_route', methods=['POST'])
def optimize_route():
    data = request.json
    start_location = data['start_location']
    end_location = data['end_location']
    mode = data['mode']
    weights = data['weights']

    # Call the run_process function and get the optimized route
    optimized_routes = run_process(start_location, end_location, mode, weights)
    
    # Return the best route and its RMSE
    return jsonify(optimized_routes[0])  # Return the route with the lowest RMSE
