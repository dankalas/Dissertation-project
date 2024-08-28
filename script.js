mapboxgl.accessToken = 'pk.eyJ1IjoiZGFuaWVsYWthbGFtdWRvIiwiYSI6ImNseW4wNno4bTAxNDAya3M0YjJqNHkwamMifQ.RXniMT8_Seus5fdPUJ2XRA';

navigator.geolocation.getCurrentPosition(successLocation, errorLocation, {
    enableHighAccuracy: true
});

function successLocation(position) {
    setupMap([position.coords.longitude, position.coords.latitude]);
}

function errorLocation() {
    console.log('Unable to retrieve your location');
    // Fallback coordinates if location retrieval fails
    setupMap([1.8882, 52.4867]);
}

function setupMap(center) {
    const map = new mapboxgl.Map({
        container: 'map', // container ID
        style: 'mapbox://styles/mapbox/streets-v12', // style URL
        center: center, // starting position [lng, lat]
        zoom: 14 // starting zoom
    });

    // Add navigation control (zoom in/out and rotate)
    const nav = new mapboxgl.NavigationControl({
        visualizePitch: true
    });
    map.addControl(nav, 'bottom-right');

    // Add geolocate control (for getting user's current location)
    map.addControl(
        new mapboxgl.GeolocateControl({
            positionOptions: {
                enableHighAccuracy: true
            },
            // When active the map will receive updates to the device's location as it changes.
            trackUserLocation: true,
            // Draw an arrow next to the location dot to indicate which direction the device is heading.
            showUserHeading: true
        })
    );

    // Add directions control (for routing and navigation)
    map.addControl(
        new MapboxDirections({
            accessToken: mapboxgl.accessToken,
            alternatives: true,  // Allow showing alternative routes
            unit: 'metric',      // Set the unit system (e.g., 'imperial' or 'metric')
            profile: 'mapbox/driving', // Set the routing profile (e.g., 'mapbox/walking', 'mapbox/cycling')
        }),
        'top-left'
    );
}
