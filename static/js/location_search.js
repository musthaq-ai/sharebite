let autocomplete;

document.addEventListener("DOMContentLoaded", () => {

    const modalElement =
        document.getElementById("locationModal");

    const input =
        document.getElementById("locationSearch");


    if (!modalElement || !input) return;


    // =====================================================
    // Initialize Google Places Autocomplete
    // =====================================================

    modalElement.addEventListener(
        "shown.bs.modal",
        () => {

            // Prevent duplicate autocomplete instances
            if (autocomplete) {

                input.focus();

                return;

            }


            if (
                typeof google === "undefined" ||
                !google.maps ||
                !google.maps.places
            ) {

                console.error(
                    "Google Places API is not loaded."
                );

                return;

            }


            autocomplete =
                new google.maps.places.Autocomplete(

                    input,

                    {

                        fields: [

                            "geometry",

                            "formatted_address",

                            "name",

                            "address_components"

                        ],

                        types: ["geocode"]

                    }

                );


            // =================================================
            // Place selected
            // =================================================

            autocomplete.addListener(
                "place_changed",
                () => {

                    const place =
                        autocomplete.getPlace();


                    if (
                        !place.geometry ||
                        !place.geometry.location
                    ) {

                        console.error(
                            "Selected place has no geometry."
                        );

                        return;

                    }


                    const latitude =
                        place.geometry.location.lat();

                    const longitude =
                        place.geometry.location.lng();


                    let locationName =
                        place.name ||
                        place.formatted_address ||
                        "Selected Location";


                    let sublocality = null;

                    let locality = null;


                    // =========================================
                    // Extract Area and City
                    // =========================================

                    if (place.address_components) {

                        place.address_components.forEach(
                            component => {

                                const types =
                                    component.types;


                                if (

                                    types.includes(
                                        "sublocality"
                                    ) ||

                                    types.includes(
                                        "sublocality_level_1"
                                    )

                                ) {

                                    sublocality =
                                        component.long_name;

                                }


                                if (

                                    types.includes(
                                        "locality"
                                    )

                                ) {

                                    locality =
                                        component.long_name;

                                }

                            }

                        );

                    }


                    // Prefer Area -> City -> Place name

                    if (sublocality) {

                        locationName = sublocality;

                    }

                    else if (locality) {

                        locationName = locality;

                    }


                    console.log(
                        "Location:",
                        locationName
                    );

                    console.log(
                        "Latitude:",
                        latitude
                    );

                    console.log(
                        "Longitude:",
                        longitude
                    );


                    // =========================================
                    // Update ALL navbar location elements
                    // =========================================

                    const navbarLocations =
                        document.querySelectorAll(
                            ".currentLocation"
                        );


                    navbarLocations.forEach(element => {

                        element.innerHTML =

                            `<i class="bi bi-geo-alt-fill"></i> ${locationName}`;

                    });


                    // =========================================
                    // Save to localStorage
                    // =========================================

                    const userLocation = {

                        name: locationName,

                        address:
                            place.formatted_address ||
                            locationName,

                        lat: latitude,

                        lng: longitude

                    };


                    localStorage.setItem(

                        "userLocation",

                        JSON.stringify(userLocation)

                    );


                    // =========================================
                    // Save to Flask session
                    // =========================================

                    fetch("/set-current-location", {

                        method: "POST",

                        headers: {

                            "Content-Type":
                                "application/json"

                        },

                        body: JSON.stringify({

                            location:
                                locationName,

                            latitude:
                                latitude,

                            longitude:
                                longitude

                        })

                    })

                    .then(response => {

                        if (!response.ok) {

                            throw new Error(
                                "Unable to save selected location."
                            );

                        }

                        return response.json();

                    })

                    .then(data => {

                        console.log(

                            "Session Location Saved:",

                            data

                        );


                        // Clear input

                        input.value = "";


                        // Close modal

                        const modal =
                            bootstrap.Modal.getInstance(
                                modalElement
                            );


                        if (modal) {

                            modal.hide();

                        }


                        /*
                         * Reload page so nearby food
                         * results are recalculated.
                         */

                        window.location.reload();

                    })

                    .catch(error => {

                        console.error(

                            "Location save error:",

                            error

                        );

                    });

                }

            );

        }

    );

});