// Mapbox access token
mapboxgl.accessToken = 'pk.eyJ1IjoiZGFuaWVsYWthbGFtdWRvIiwiYSI6ImNseW4wNno4bTAxNDAya3M0YjJqNHkwamMifQ.RXniMT8_Seus5fdPUJ2XRA';
const APP_STORE = {};
let previousControl = null;
class OptimizedRoutesControl {
    constructor(routeResults = []) {
        this.routeResults = routeResults
    }
    onAdd(map) {
        this.map = map;
        this.container = document.createElement('div');
        this.container.className = 'mapboxgl-ctrl scrollable-list-container bg-light-subtle';
        this.container.style.width = '250px';
        this.container.style.maxHeight = '90vh';
        this.container.style.overflowY = 'auto';
        this.container.style.backgroundColor = '#f8f8f8';
        this.container.style.borderLeft = '1px solid #ccc';
        this.container.style.padding = '10px';
        this.container.classList.add('container');
        
        let innerHTML =  this.routeResults.map(route =>{
           const inner = Object.entries(route).map(([key, value]) => {
                return `<li class="list-group-item">
                    <p>${key}</p>
                    <p class="flex-fill">${value}</p>
                </li>`
            }).join('\n')

            return `
            <h4>${route["Route Label"]}</h4>
            <ul class="list-group">${inner}</ul>`;
        }).join('<hr>')
        this.container.innerHTML = innerHTML;
        return this.container;
    }

    onRemove() {
        this.container.parentNode.removeChild(this.container);
        this.map = undefined;
        
    }
}



// Initialize user weights object
let userWeights = {};
let directionsControl;  // Declare this globally to modify it later
let selectedMode = 'cycling';  // Default mode

// Handle form submission for weight inputs
document.getElementById('weight-form').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent the default form submission

    // Collect the mode selected by the user
    selectedMode = document.getElementById('mode-select').value;

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
    console.log('Selected Mode:', selectedMode);

    // Update the directions profile based on the selected mode
    directionsControl.setProfile(`mapbox/${selectedMode}`);
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

// Setup map with the initial mode
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

    // Initialize Mapbox Directions with the default mode
    directionsControl = new MapboxDirections({
        accessToken: mapboxgl.accessToken,
        alternatives: true,
        unit: 'metric',
        profile: `mapbox/${selectedMode}`,  // Use the default selected mode here
    });

    map.addControl(directionsControl, 'top-left');

    directionsControl.on('route', function(event) {
        const routes = event.route;
        const start_location = routes[0].legs[0].steps[0].maneuver.location.join(',');
        const end_location = routes[0].legs[0].steps.slice(-1)[0].maneuver.location.join(',');
        const start_location_name = routes[0].legs[0].summary;
        const end_location_name = routes[0].legs.slice(-1)[0].summary;
        if(previousControl !== null) {
            map.removeControl(previousControl);
            previousControl = null;
        }
        console.log(routes[0]);
        $("#loadingModal").modal("show")

        // Send data to the Flask server with user-selected weights
        fetch('/optimize_route', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                start_location: start_location,
                end_location: end_location,
                mode: selectedMode,  // Use the selected mode here
                start_location_name, 
                end_location_name,
                weights: userWeights  // Use the user-selected weights
            })
        })
        .then(response => response.json())
        .then(response => {
            const optimizedRoutes = response.optimized_routes
            const optimizedRouteControl = new OptimizedRoutesControl(optimizedRoutes);
            APP_STORE.optimizedRoutes = optimizedRoutes;
      
            $("#loadingModal").modal("hide")
            map.addControl(optimizedRouteControl, 'top-right');
            previousControl = optimizedRouteControl;
          
            
        })
        .catch(error => {console.error('Error:', error);  $("#loadingModal").modal("hide");});
    });
}
