// Mapbox access token
mapboxgl.accessToken = 'pk.eyJ1IjoiZGFuaWVsYWthbGFtdWRvIiwiYSI6ImNseW4wNno4bTAxNDAya3M0YjJqNHkwamMifQ.RXniMT8_Seus5fdPUJ2XRA';
const APP_STORE = {};
let previousControl = null;

const toolTipMap = {
    'AQI': 'this index represents the amount of air pollution and its potential benefits. A score of 0-50 is good, 51-100 is moderate and over 100 is unhealthy',
    'Time (minutes)': 'This represents how long a route/journey would take to arrive at a destination. This is measured in minutes. Please divide by 60 to get the time in hours',
    'Distance (km)': 'This represents how far is needed to be covered to arrive at a destination. This is measured in kilometres(km)',
    'Safety Rating': 'This represents how safe a particular route is historically.',
    'Carbon Footprint (g CO2)': 'this represents how much carbon is emitted contributing to climate change. This is measured in Co2.',
    'Calories Burned': 'this represents the number of calories used up by the user on a specific route. This is measured in kilos.',
    'Noise Pollution (dB)': 'this represents the average amount of noise pollutants are present across the route.',
    'Scenic Score': 'This represents how aesthetically pleasant a particular route is historically.',
}
class OptimizedRoutesControl {
    constructor(routeResults = []) {
        this.routeResults = routeResults
    }
    onAdd(map) {
        this.map = map;
        this.container = document.createElement('div');
        this.container.id = "route-summary";
        this.container.className = 'mapboxgl-ctrl scrollable-list-container bg-light-subtle';
        this.container.style.width = '300px';
        this.container.style.maxHeight = '90vh';
        this.container.style.overflowY = 'auto';
        this.container.style.backgroundColor = '#f8f8f8';
        this.container.style.borderLeft = '1px solid #ccc';
        this.container.style.padding = '10px';
        this.container.classList.add('container');

        let innerHTML = this.routeResults.map((route, index) => {

            const inner = Object.entries(route).map(([key, value]) => {
                console.log(`Tooltip for ${key} is `, toolTipMap[key])
                return `  <li class="list-group-item d-flex align-items-center"><p class="mb-0 flex-fill">${key}</p>
        <p class="mb-0">
            ${value}
        </p>
        <span class="span-icon" data-toggle="tooltip" data-placement="left" title="${toolTipMap[key] || ''}">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="16" x2="12" y2="12"></line>
              <line x1="12" y1="8" x2="12.01" y2="8"></line>
            </svg>
          </span>
        </li>`
            }).join('\n')

            return `
            <div class="accordion-item">
                <h2 class="accordion-header">
      <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapse${index + 1}" aria-expanded="${index === 0}" aria-controls="collapse${index + 1}">
      ${route["Route Label"]}
      ${index === 0 ? '<span style="margin-left: 5px" class="badge bg-primary">Recommended</span>' : ''}
      </button>
    </h2>
           <div id="collapse${index + 1}" class="accordion-collapse collapse ${index === 0 ? 'show' : ''}" data-bs-parent="#resultsAccordion">
      <div class="accordion-body">
             <ul class="list-group">${inner}</ul>
      </div>
    </div>
            
     
            </div>`;
        }).join('\n');
        this.container.innerHTML = `<div>
        <h6 class="mb-3">The  Routes listed below are Ranked in the order of their suitability to your Predefined preferences and contain Key information about each Route</h6>
        
        <div class="accordion" id="resultsAccordion">${innerHTML}</div></div>`;
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
document.getElementById('weight-form').addEventListener('submit', function (event) {
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

    directionsControl.on('route', function (event) {
        const routes = event.route;
        const start_location = routes[0].legs[0].steps[0].maneuver.location.join(',');
        const end_location = routes[0].legs[0].steps.slice(-1)[0].maneuver.location.join(',');
        const start_location_name = routes[0].legs[0].summary;
        const end_location_name = routes[0].legs.slice(-1)[0].summary;
        if (previousControl !== null) {
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
                const excludedColumns = 'Norm AQI,Norm Calories,Norm Carbon,Norm Distance,Norm Noise,Norm Scenic,Norm Safety Rating,Norm Time,RMSE'.split(',')
                for (const route of optimizedRoutes) {
                    for (const column of excludedColumns) {
                        delete route[column];
                    }
                }
                const optimizedRouteControl = new OptimizedRoutesControl(optimizedRoutes);
                APP_STORE.optimizedRoutes = optimizedRoutes;

                $("#loadingModal").modal("hide")
                map.addControl(optimizedRouteControl, 'top-right');
                previousControl = optimizedRouteControl;


            })
            .catch(error => { console.error('Error:', error); $("#loadingModal").modal("hide"); });
    });
}
