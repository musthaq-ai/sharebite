document.addEventListener("DOMContentLoaded", () => {

    const locationText = document.getElementById("currentLocation");

    if (!locationText) return;

    // ==========================================
    // Check if location is already saved
    // ==========================================

    const savedLocation = localStorage.getItem("userLocation");

    if (savedLocation) {

        try {

            const location = JSON.parse(savedLocation);

            locationText.innerHTML =
                `<i class="bi bi-geo-alt-fill"></i> ${location.name}`;

            console.log("Using saved location:", location.name);

            // Stop here.
            return;

        } catch (e) {

            localStorage.removeItem("userLocation");

        }

    }

    // ==========================================
    // Browser Support
    // ==========================================

    if (!navigator.geolocation) {

        locationText.innerText = "Location not supported";

        return;

    }

    locationText.innerText = "Getting location...";

    // ==========================================
    // Get Current GPS Location
    // ==========================================

    navigator.geolocation.getCurrentPosition(

        function(position) {

            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;

            console.log("Latitude :", latitude);
            console.log("Longitude:", longitude);

            fetch("/get-location", {

                method: "POST",

                headers: {

                    "Content-Type": "application/json"

                },

                body: JSON.stringify({

                    latitude: latitude,
                    longitude: longitude

                })

            })

            .then(response => response.json())

            .then(data => {

                console.log(data);

                if (data.success) {

                    locationText.innerHTML =
                        `<i class="bi bi-geo-alt-fill"></i> ${data.location}`;

                    // ==========================================
                    // Save Location
                    // ==========================================

                    localStorage.setItem(

                        "userLocation",

                        JSON.stringify({

                            name: data.location,

                            lat: latitude,

                            lng: longitude

                        })

                    );

                }

                else {

                    locationText.innerText = "Unknown Location";

                }

            })

            .catch(error => {

                console.error(error);

                locationText.innerText = "Unable to fetch location";

            });

        },

        function(error) {

            switch(error.code){

                case error.PERMISSION_DENIED:

                    locationText.innerText = "Permission Denied";
                    break;

                case error.POSITION_UNAVAILABLE:

                    locationText.innerText = "Location Unavailable";
                    break;

                case error.TIMEOUT:

                    locationText.innerText = "Request Timed Out";
                    break;

                default:

                    locationText.innerText = "Unable to fetch location";

            }

        },

        {

            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 0

        }

    );

});