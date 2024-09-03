let map;
let userLocation;

function initMap() {
    // Check if geolocation is available
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            userLocation = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };

            // Initialize the map centered on the user's current location
            map = new google.maps.Map(document.getElementById("map"), {
                zoom: 14,
                center: userLocation,
            });

            // Add a marker at the user's location
            new google.maps.Marker({
                position: userLocation,
                map: map,
                title: "You are here"
            });

            // Add click listeners for the search buttons
            document.getElementById("find-ngos").addEventListener("click", () => findNearbyPlaces("NGO", '#4CAF50'));
            document.getElementById("find-hospitals").addEventListener("click", () => findNearbyPlaces("hospital", '#007BFF'));
            document.getElementById("find-blood-donation-camps").addEventListener("click", () => findNearbyPlaces("blood donation", '#FF5733'));
            document.getElementById("find-schools").addEventListener("click", () => findNearbyPlaces("school", '#FFC300'));

        }, function() {
            handleLocationError(true);
        });
    } else {
        // Browser doesn't support Geolocation
        handleLocationError(false);
    }
}

function findNearbyPlaces(type, color) {
    const request = {
        location: userLocation,
        radius: 20000, // 20 km radius
        keyword: type
    };

    const service = new google.maps.places.PlacesService(map);
    service.nearbySearch(request, function(results, status) {
        if (status === google.maps.places.PlacesServiceStatus.OK) {
            results.forEach(function(place) {
                createMarker(place, color);
            });
        } else {
            alert(`No ${type}s found in your area.`);
        }
    });
}

function createMarker(place, color) {
    const placeLoc = place.geometry.location;
    const marker = new google.maps.Marker({
        map: map,
        position: placeLoc,
        title: place.name,
        icon: {
            path: google.maps.SymbolPath.CIRCLE,
            scale: 10,
            fillColor: color,
            fillOpacity: 1,
            strokeWeight: 2,
            strokeColor: '#FFFFFF'
        }
    });

    const infowindow = new google.maps.InfoWindow({
        content: `<strong>${place.name}</strong><br>${place.vicinity}`
    });

    marker.addListener("click", function() {
        infowindow.open(map, marker);
    });
}

function handleLocationError(browserHasGeolocation) {
    alert(browserHasGeolocation
        ? "Error: The Geolocation service failed."
        : "Error: Your browser doesn't support geolocation.");
}
