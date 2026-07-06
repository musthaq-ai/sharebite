let autocomplete;

document.addEventListener("DOMContentLoaded", () => {

    const modalElement = document.getElementById("locationModal");
    const input = document.getElementById("locationSearch");

    if (!modalElement || !input) return;

    modalElement.addEventListener("shown.bs.modal", () => {

        // Prevent creating multiple autocomplete instances
        if (autocomplete) return;

        autocomplete = new google.maps.places.Autocomplete(input, {

            fields: [
                "geometry",
                "formatted_address",
                "name",
                "address_components"
            ],

            types: ["geocode"]

        });

        autocomplete.addListener("place_changed", () => {

            const place = autocomplete.getPlace();

            if (!place.geometry) return;

            const latitude = place.geometry.location.lat();
            const longitude = place.geometry.location.lng();

            let locationName = place.name;

            // Prefer Area -> City -> Name
            if (place.address_components) {

                place.address_components.forEach(component => {

                    if (component.types.includes("sublocality") ||
                        component.types.includes("sublocality_level_1")) {

                        locationName = component.long_name;

                    }
                    else if (component.types.includes("locality")) {

                        locationName = component.long_name;

                    }

                });

            }

            console.log("Location :", locationName);
            console.log("Latitude :", latitude);
            console.log("Longitude:", longitude);

            // Update navbar
            const navbarLocation = document.getElementById("currentLocation");

            if (navbarLocation) {

                navbarLocation.innerHTML =
                    `<i class="bi bi-geo-alt-fill"></i> ${locationName}`;

            }

            // Save for future use
            localStorage.setItem("userLocation", JSON.stringify({

    name: locationName,

    address: place.formatted_address || locationName,

    lat: latitude,

    lng: longitude

}));

            // Clear search box
            input.value = "";

            // Close modal
            const modal = bootstrap.Modal.getInstance(modalElement);

            if (modal) {

                modal.hide();

            }

        });

    });

});