document.addEventListener("DOMContentLoaded", () => {

    const locationElements = document.querySelectorAll(".currentLocation");

    if (locationElements.length === 0) return;

    // ==========================================
    // Check if location is already saved
    // ==========================================

    const savedLocation = localStorage.getItem("userLocation");

    if (savedLocation) {

        try {

            const location = JSON.parse(savedLocation);

            locationElements.forEach(el => {

                el.innerHTML =
                    `<i class="bi bi-geo-alt-fill"></i> ${location.name}`;

            });

            console.log("Using saved location:", location.name);

            return;

        }

        catch (e) {

            localStorage.removeItem("userLocation");

        }

    }

    // ==========================================
    // Browser Support
    // ==========================================

    if (!navigator.geolocation) {

        locationElements.forEach(el => {

            el.innerText = "Location not supported";

        });

        return;

    }

    locationElements.forEach(el => {

        el.innerText = "Getting location...";

    });

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

                    locationElements.forEach(el => {

                        el.innerHTML =
                            `<i class="bi bi-geo-alt-fill"></i> ${data.location}`;

                    });

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

                    // ==========================================
                    // Save Current Location to Flask Session
                    // ==========================================

                    fetch("/set-current-location", {

                        method: "POST",

                        headers: {

                            "Content-Type": "application/json"

                        },

                        body: JSON.stringify({

                            location: data.location,

                            latitude: latitude,

                            longitude: longitude

                        })

                    })

                    .then(res => res.json())

                    .then(() => {

                        console.log("Current location saved in session.");

                    })

                    .catch(err => {

                        console.error(err);

                    });

                }

                else {

                    locationElements.forEach(el => {

                        el.innerText = "Unknown Location";

                    });

                }

            })

            .catch(error => {

                console.error(error);

                locationElements.forEach(el => {

                    el.innerText = "Unable to fetch location";

                });

            });

        },

        function(error) {

            let message = "Unable to fetch location";

            switch(error.code){

                case error.PERMISSION_DENIED:

                    message = "Permission Denied";
                    break;

                case error.POSITION_UNAVAILABLE:

                    message = "Location Unavailable";
                    break;

                case error.TIMEOUT:

                    message = "Request Timed Out";
                    break;

            }

            locationElements.forEach(el => {

                el.innerText = message;

            });

        },

        {

            enableHighAccuracy: true,

            timeout: 10000,

            maximumAge: 0

        }

    );

});