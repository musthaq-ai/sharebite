document.addEventListener("DOMContentLoaded", () => {

    const locationElements =
        document.querySelectorAll(".currentLocation");

    const currentLocationBtn =
        document.getElementById("useCurrentLocation");


    // =====================================================
    // Update all navbar location elements
    // =====================================================

    function updateNavbarLocation(locationName) {

        locationElements.forEach(element => {

            element.innerHTML =
                `<i class="bi bi-geo-alt-fill"></i> ${locationName}`;

        });

    }


    // =====================================================
    // Show status in navbar
    // =====================================================

    function showLocationStatus(message) {

        locationElements.forEach(element => {

            element.innerText = message;

        });

    }


    // =====================================================
    // Close location modal
    // =====================================================

    function closeLocationModal() {

        const modalElement =
            document.getElementById("locationModal");

        if (!modalElement) return;

        const modal =
            bootstrap.Modal.getInstance(modalElement);

        if (modal) {

            modal.hide();

        }

    }


    // =====================================================
    // Save location to Flask session
    // =====================================================

    function saveLocationToSession(
        locationName,
        latitude,
        longitude
    ) {

        return fetch("/set-current-location", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({

                location: locationName,

                latitude: latitude,

                longitude: longitude

            })

        })

        .then(response => {

            if (!response.ok) {

                throw new Error(
                    "Unable to save location in session."
                );

            }

            return response.json();

        });

    }


    // =====================================================
    // Reverse geocode GPS coordinates
    // =====================================================

    function processCoordinates(latitude, longitude, shouldReload = false) {

        console.log("Latitude:", latitude);
        console.log("Longitude:", longitude);

        return fetch("/get-location", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({

                latitude: latitude,

                longitude: longitude

            })

        })

        .then(response => {

            if (!response.ok) {

                throw new Error(
                    "Unable to get location name."
                );

            }

            return response.json();

        })

        .then(data => {

            if (!data.success) {

                throw new Error(
                    "Location could not be identified."
                );

            }

            const locationName = data.location;

            // Update navbar immediately
            updateNavbarLocation(locationName);


            // Save in localStorage
            const userLocation = {

                name: locationName,

                lat: latitude,

                lng: longitude

            };

            localStorage.setItem(

                "userLocation",

                JSON.stringify(userLocation)

            );


            // Save to Flask session
            return saveLocationToSession(

                locationName,

                latitude,

                longitude

            )

            .then(sessionData => {

                console.log(
                    "Current location saved in session:",
                    sessionData
                );

                closeLocationModal();


                /*
                 * When user explicitly clicks
                 * "Use Current Location",
                 * reload so nearby food is recalculated.
                 */

                if (shouldReload) {

                    window.location.reload();

                }

            });

        });

    }


    // =====================================================
    // Get GPS location
    // =====================================================

    function getCurrentGPSLocation(shouldReload = false) {

        if (!navigator.geolocation) {

            showLocationStatus(
                "Location not supported"
            );

            return;

        }


        showLocationStatus(
            "Getting location..."
        );


        // Disable button while detecting
        if (currentLocationBtn) {

            currentLocationBtn.disabled = true;

            currentLocationBtn.innerHTML = `

                <span
                    class="spinner-border spinner-border-sm me-2"
                    role="status">
                </span>

                Detecting Location...

            `;

        }


        navigator.geolocation.getCurrentPosition(

            function(position) {

                const latitude =
                    position.coords.latitude;

                const longitude =
                    position.coords.longitude;


                processCoordinates(

                    latitude,

                    longitude,

                    shouldReload

                )

                .catch(error => {

                    console.error(error);

                    showLocationStatus(
                        "Unable to fetch location"
                    );

                    resetCurrentLocationButton();

                });

            },


            function(error) {

                console.error(
                    "Geolocation error:",
                    error
                );

                let message =
                    "Unable to fetch location";


                switch (error.code) {

                    case error.PERMISSION_DENIED:

                        message =
                            "Location permission denied";

                        break;


                    case error.POSITION_UNAVAILABLE:

                        message =
                            "Location unavailable";

                        break;


                    case error.TIMEOUT:

                        message =
                            "Location request timed out";

                        break;

                }


                showLocationStatus(message);

                resetCurrentLocationButton();

            },


            {

                enableHighAccuracy: true,

                timeout: 15000,

                maximumAge: 0

            }

        );

    }


    // =====================================================
    // Reset current-location button
    // =====================================================

    function resetCurrentLocationButton() {

        if (!currentLocationBtn) return;

        currentLocationBtn.disabled = false;

        currentLocationBtn.innerHTML = `

            <i class="bi bi-crosshair"></i>

            Use Current Location

        `;

    }


    // =====================================================
    // Use Current Location button click
    // =====================================================

    if (currentLocationBtn) {

        currentLocationBtn.addEventListener(

            "click",

            function(event) {

                event.preventDefault();

                /*
                 * true = reload after successful GPS detection,
                 * allowing nearby food results to refresh.
                 */

                getCurrentGPSLocation(true);

            }

        );

    }


    // =====================================================
    // On page load: use saved location if available
    // =====================================================

    const savedLocation =
        localStorage.getItem("userLocation");


    if (savedLocation) {

        try {

            const location =
                JSON.parse(savedLocation);


            if (
                location.name &&
                location.lat !== undefined &&
                location.lng !== undefined
            ) {

                updateNavbarLocation(
                    location.name
                );

                console.log(
                    "Using saved location:",
                    location.name
                );

                return;

            }

        }

        catch (error) {

            console.error(
                "Invalid saved location:",
                error
            );

        }


        localStorage.removeItem(
            "userLocation"
        );

    }


    // =====================================================
    // No saved location: automatically detect GPS
    // =====================================================

    getCurrentGPSLocation(false);

});