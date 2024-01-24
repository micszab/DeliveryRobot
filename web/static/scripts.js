// static/scripts.js

const socket = io();
var routeLegs = '';

function openContainer() {
	socket.emit('open_box');
}

function switchLights() {
	socket.emit('switch_lights');
}

function move(direction) {
	socket.emit('move', direction);
}

function stopMotors() {
	socket.emit('stop_motors');
}

function switchMode(mode) {
	alert("switch mode");
	socket.emit('switch_mode', mode);
}

function startJourney() {
	var telephoneNumber = document.getElementById("number-input").value;
	// Check if the value contains '+' and numbers
	if (telephoneNumber.includes('+') && /\d/.test(telephoneNumber)) {
		alert("Telephone is valid");
	} else {
		alert("Telephone must contain '+' and numbers");
	}
	socket.emit('start_journey', telephoneNumber, routeLegs);
}

const localVideo = document.getElementById('camera');
const startButton = document.getElementById('start-stream');
const stopButton = document.getElementById('stop-stream');

function startCameraStream() {	
	startButton.disabled = true;
	stopButton.disabled = false;

	socket.emit('startStreaming');
}

function stopCameraStream() {
	socket.emit('stopStreaming');

	startButton.disabled = false;
	stopButton.disabled = true;
}

var map;
var directionsService;
var directionsRenderer;
var waypoints = [];
var robotLocation = { lat: 50.09910, lng: 19.9552 };
var robotMarker;

function updateMarkerCoordinates(coordinates) {
    var newCoordinates = new google.maps.LatLng(coordinates['lat'], coordinates['lng']);
    robotMarker.setPosition(newCoordinates);
}

function updateMapWithGPSData() {
    // Make an AJAX request to get GPS data from the server
    fetch('/get_gps_data')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
		robotLocation = {
                lat: data.latitude,
                lng: data.longitude
            };

            updateMarkerCoordinates(robotLocation);

        })
        .catch(error => {
            console.error('Error fetching GPS data:', error);
        });
}

function initMap() {
	console.log("init map");
      // Create a new map instance
	map = new google.maps.Map(document.getElementById("map"), {
        	center: robotLocation,
        	zoom: 17 // Adjust the zoom level as needed
	});

	robotMarker = new google.maps.Marker({
		position: robotLocation,
		map: map,
		title: 'Robot Location'})

	directionsService = new google.maps.DirectionsService();
	directionsRenderer = new google.maps.DirectionsRenderer({
        	map: map,
		draggable: true
	});

	google.maps.event.addListener(map, 'click', function(event) {
		addWaypoint(event.latLng);
	});

	// Initialize the Places Autocomplete service
	var input = document.getElementById('addressInput');
	var autocomplete = new google.maps.places.Autocomplete(input);

	updateMapWithGPSData();
	map.setCenter(robotLocation);
	setInterval(updateMapWithGPSData, 10000);
}
	
function addWaypoint(location) {
	waypoints.push({
		location: location,
		stopover: true
        });
	
	updateRoute();
}

function updateRoute() {
	if (waypoints.length >= 1) {
		var request = {
			origin: robotLocation,
			destination: waypoints[0].location,
			waypoints: [],
			optimizeWaypoints: true,
			travelMode: 'WALKING'
		};

		directionsService.route(request, function(response, status) {
			if (status === 'OK') {
				directionsRenderer.setDirections(response);
				routeLegs = response.routes[0].legs;
				console.log(routeLegs);
			} else {
				window.alert('Directions request failed due to ' + status);
			}
		});
	}
}

function searchAddress() {
	var addressInput = document.getElementById('addressInput');
	var geocoder = new google.maps.Geocoder();

	geocoder.geocode({ address: addressInput.value }, function(results, status) {
		if (status === 'OK' && results[0]) {
			map.setCenter(results[0].geometry.location);
			addWaypoint(results[0].geometry.location);
		} else {
			alert('Geocode was not successful for the following reason: ' + status);
		}
	});
}

