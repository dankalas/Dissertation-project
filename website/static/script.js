// Mapbox access token
mapboxgl.accessToken = 'pk.eyJ1IjoiZGFuaWVsYWthbGFtdWRvIiwiYSI6ImNseW4wNno4bTAxNDAya3M0YjJqNHkwamMifQ.RXniMT8_Seus5fdPUJ2XRA';

// Initialize user weights object
let userWeights = {};

// Handle form submission for weight inputs
document.getElementById('weight-form').addEventListener('submit', function(event) {
    console.log("this is running")
    event.preventDefault();  // Prevent the default form submission

    // Collect the weights entered by the user
    userWeights = {
        "Norm Time": parseFloat(document.getElementById('time-weight').value),
        "Norm Distance": parseFloat(document.getElementById('distance-weight').value),
        "Norm Calories": parseFloat(document.getElementById('calories-weight').value),
        "Norm Carbon": parseFloat(document.getElementById('carbon-weight').value),
        "Norm Noise": parseFloat(document.getElementById('noise-weight').value),
        "Norm Scenic": parseFloat(document.getElementById('scenic-weight').value),
        "Norm AQI": parseFloat(document.getElementById('aqi-weight').value),
        "Norm Safety Rating": parseFloat(document.getElementById('safety-weight').value)
    };

    console.log('User Weights:', userWeights);
});

// Geolocation and map setup
navigator.geolocation.getCurrentPosition(successLocation, errorLocation, {
    enableHighAccuracy: true
});

function successLocation(position) {
    setupMap([position.coords.longitude, position.coords.latitude]);
}

function errorLocation() {
    console.log('Unable to retrieve your location');
    setupMap([1.8882, 52.4867]);  // Fallback coordinates
}

function setupMap(center) {
    const map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/streets-v12',
        center: center,
        zoom: 14
    });

    const nav = new mapboxgl.NavigationControl({ visualizePitch: true });
    map.addControl(nav, 'bottom-right');

    map.addControl(
        new mapboxgl.GeolocateControl({
            positionOptions: { enableHighAccuracy: true },
            trackUserLocation: true,
            showUserHeading: true
        })
    );

    const directions = new MapboxDirections({
        accessToken: mapboxgl.accessToken,
        alternatives: true,
        unit: 'metric',
        profile: 'mapbox/cycling',
    });

    map.addControl(directions, 'top-left');

    directions.on('route', function(event) {
        const routes = event.route;
        const start_location = routes[0].legs[0].steps[0].maneuver.location.join(',');
        const end_location = routes[0].legs[0].steps.slice(-1)[0].maneuver.location.join(',');

        // Send data to the Flask server with user-selected weights
        fetch('/optimize_route', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                start_location: start_location,
                end_location: end_location,
                mode: 'cycling',
                weights: userWeights  // Use the user-selected weights
            })
        })
        .then(response => response.json())
        .then(data => {
            const bestRoute = data['First Row'];
            const coordinates = bestRoute['route_geometry'];

            // Add the optimized route to the map
            map.addLayer({
                id: 'optimized-route',
                type: 'line',
                source: {
                    type: 'geojson',
                    data: {
                        type: 'Feature',
                        properties: {},
                        geometry: {
                            type: 'LineString',
                            coordinates: coordinates
                        }
                    }
                },
                layout: {
                    'line-join': 'round',
                    'line-cap': 'round'
                },
                paint: {
                    'line-color': '#ff0000',
                    'line-width': 8
                }
            });
        })
        .catch(error => console.error('Error:', error));
    });
}
