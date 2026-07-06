let map;
let marker;
let geocoder;
let pickupAutocomplete;

window.addEventListener("load", () => {

    if (typeof google === "undefined") {

        console.error("Google Maps not loaded.");

        return;

    }

    initGoogleMap();

});

function initGoogleMap() {

    const mapDiv = document.getElementById("googleMap");

    if (!mapDiv) return;

    geocoder = new google.maps.Geocoder();

    // ------------------------------------
// Default Location
// ------------------------------------

// =========================================
// Priority:
// 1. Existing Donation (Edit)
// 2. Navbar Selected Location
// 3. Default Location
// =========================================

const savedLat = document.getElementById("latitude");
const savedLng = document.getElementById("longitude");

let defaultLocation = {

    lat: 10.7905,

    lng: 78.7047

};

// ------------------------------
// Edit Donation
// ------------------------------

if (

    savedLat &&
    savedLng &&
    savedLat.value &&
    savedLng.value

){

    defaultLocation = {

        lat: parseFloat(savedLat.value),

        lng: parseFloat(savedLng.value)

    };

}

// ------------------------------
// Navbar Selected Location
// ------------------------------

else{

    const navbarLocation = localStorage.getItem("userLocation");

    if(navbarLocation){

        const loc = JSON.parse(navbarLocation);

        defaultLocation = {

            lat: loc.lat,

            lng: loc.lng

        };

    }

}
    map = new google.maps.Map(mapDiv, {

        center: defaultLocation,

        zoom: 14,

        mapTypeControl: false,

        streetViewControl: false,

        fullscreenControl: false

    });

    marker = new google.maps.Marker({

        position: defaultLocation,

        map: map,

        draggable: true,

        animation: google.maps.Animation.DROP

    });

    // ------------------------------------
    // Marker Drag
    // ------------------------------------

    marker.addListener("dragend", () => {

        const pos = marker.getPosition();

        updateLocation(

            pos.lat(),

            pos.lng()

        );

    });

    // ------------------------------------
    // Click Map
    // ------------------------------------

    map.addListener("click", (event) => {

        marker.setPosition(event.latLng);

        updateLocation(

            event.latLng.lat(),

            event.latLng.lng()

        );

    });

    // ------------------------------------
    // Google Search
    // ------------------------------------

    const input = document.getElementById("pickupSearch");

    if (input) {

       pickupAutocomplete = new google.maps.places.pickupAutocomplete(input,{

    fields:[

        "geometry",

        "formatted_address",

        "name"

    ]

});

        pickupAutocomplete.bindTo("bounds", map);

        pickupAutocomplete.addListener("place_changed", () => {

            const place = pickupAutocomplete.getPlace();

            if (!place.geometry) return;

            map.panTo(place.geometry.location);

            map.setZoom(17);

            marker.setPosition(place.geometry.location);

            updateLocation(

                place.geometry.location.lat(),

                place.geometry.location.lng()

            );

        });

    }

    // ------------------------------------
    // Current Location Automatically
    // ------------------------------------
// =====================================
// If no saved location exists,
// use GPS once.
// =====================================

if(!localStorage.getItem("userLocation")){

    if(navigator.geolocation){

        navigator.geolocation.getCurrentPosition(

            (position)=>{

                const lat = position.coords.latitude;

                const lng = position.coords.longitude;

                const current = {

                    lat,

                    lng

                };

                map.setCenter(current);

                marker.setPosition(current);

                updateLocation(lat,lng);

            }

        );

    }

}
else{

    marker.setPosition(defaultLocation);

    map.setCenter(defaultLocation);

    updateLocation(

        defaultLocation.lat,

        defaultLocation.lng

    );

}
    
    // ------------------------------------
    // Use Current Location Button
    // ------------------------------------
// ------------------------------------
// Use Current Location Button
// ------------------------------------

const currentBtn = document.getElementById("currentLocationBtn");

if (currentBtn) {

    currentBtn.addEventListener("click", () => {

        if (!navigator.geolocation) return;

        navigator.geolocation.getCurrentPosition(

            (position) => {

                const lat = position.coords.latitude;
                const lng = position.coords.longitude;

                const current = {

                    lat: lat,
                    lng: lng

                };

                map.panTo(current);

                map.setZoom(17);

                marker.setPosition(current);

                updateLocation(lat, lng);

                // =====================================
                // Save as the current selected location
                // =====================================

                reverseGeocode(lat, lng, true);

            },

            (error) => {

                console.error(error);

                alert("Unable to fetch your current location.");

            }

        );

    });

}

// ======================================================
// Update Location
// ======================================================

function updateLocation(lat, lng) {

    // Hidden inputs
    const latInput = document.getElementById("latitude");
    const lngInput = document.getElementById("longitude");

    // Display inputs
    const latDisplay = document.getElementById("latitude_display");
    const lngDisplay = document.getElementById("longitude_display");

    if(latInput){

        latInput.value = lat.toFixed(6);

    }

    if(lngInput){

        lngInput.value = lng.toFixed(6);

    }

    if(latDisplay){

        latDisplay.value = lat.toFixed(6);

    }

    if(lngDisplay){

        lngDisplay.value = lng.toFixed(6);

    }

    reverseGeocode(lat,lng);

}
// ======================================================
// Reverse Geocoding
// ======================================================

// ======================================================
// Reverse Geocoding
// ======================================================

function reverseGeocode(lat, lng, saveToLocalStorage = false) {

    geocoder.geocode(

        {
            location: {
                lat: lat,
                lng: lng
            }
        },

        (results, status) => {

            if (status === "OK" && results[0]) {

                const address = results[0].formatted_address;

                // ------------------------------------
                // Hidden Address (Submitted to Flask)
                // ------------------------------------

                const hiddenAddress =
                    document.getElementById("formattedAddress");

                if (hiddenAddress) {

                    hiddenAddress.value = address;

                }

                // ------------------------------------
                // Display Address
                // ------------------------------------

                const displayAddress =
                    document.getElementById("addressDisplay");

                if (displayAddress) {

                    displayAddress.value = address;

                }

                // ------------------------------------
                // Save Selected Location
                // ------------------------------------

                if (saveToLocalStorage) {

                    let locationName = address;

                    // Prefer locality or sublocality
                    if (results[0].address_components) {

                        results[0].address_components.forEach(component => {

                            if (
                                component.types.includes("sublocality") ||
                                component.types.includes("sublocality_level_1")
                            ) {

                                locationName = component.long_name;

                            }
                            else if (
                                component.types.includes("locality")
                            ) {

                                locationName = component.long_name;

                            }

                        });

                    }

                    localStorage.setItem(

                        "userLocation",

                        JSON.stringify({

                            name: locationName,

                            address: address,

                            lat: lat,

                            lng: lng

                        })

                    );

                    // ------------------------------------
                    // Update Navbar Immediately
                    // ------------------------------------

                    const navbarLocation =
                        document.getElementById("currentLocation");

                    if (navbarLocation) {

                        navbarLocation.innerHTML =
                            `<i class="bi bi-geo-alt-fill"></i> ${locationName}`;

                    }

                }

            }

            else {

                console.error("Reverse Geocoding Failed:", status);

            }

        }

    );

}
}