// ==========================================
// IMAGE PREVIEW
// ==========================================

const imageInput = document.getElementById("imageInput");

if (imageInput) {

    imageInput.addEventListener("change", function (e) {

        const file = e.target.files[0];

        if (file) {

            document.getElementById("previewImage").src =
                URL.createObjectURL(file);

        }

    });

}

// ==========================================
// LEAFLET MAP
// ==========================================

const mapContainer = document.getElementById("map");

if (mapContainer) {

    // Default Location (Tamil Nadu)
    const map = L.map("map").setView([11.1271, 78.6569], 7);

    L.tileLayer(
        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        {
            attribution: "&copy; OpenStreetMap contributors"
        }
    ).addTo(map);

    let marker = null;

    // ----------------------------
    // Update Coordinates
    // ----------------------------

    function updateCoordinates(lat, lng) {

        // Hidden fields (submitted to Flask)

        document.getElementById("latitude").value = lat;
        document.getElementById("longitude").value = lng;

        // Visible fields (for debugging)

        const latDisplay = document.getElementById("latitude_display");
        const lngDisplay = document.getElementById("longitude_display");

        if (latDisplay)
            latDisplay.value = lat;

        if (lngDisplay)
            lngDisplay.value = lng;

    }

    // ----------------------------
    // Place Marker
    // ----------------------------

    function placeMarker(lat, lng) {

        if (marker) {

            map.removeLayer(marker);

        }

        marker = L.marker(
            [lat, lng],
            {
                draggable: true
            }
        ).addTo(map);

        updateCoordinates(lat, lng);

        marker.on("dragend", function (e) {

            const pos = e.target.getLatLng();

            updateCoordinates(
                pos.lat,
                pos.lng
            );

        });

    }

    // ==========================================
    // LOAD SAVED LOCATION (EDIT PAGE)
    // ==========================================

    const savedLat =
        document.getElementById("latitude").value;

    const savedLng =
        document.getElementById("longitude").value;

    if (savedLat && savedLng) {

        map.setView(
            [savedLat, savedLng],
            16
        );

        placeMarker(
            savedLat,
            savedLng
        );

    }

    // ==========================================
    // CLICK ON MAP
    // ==========================================

    map.on("click", function (e) {

        const lat = e.latlng.lat;

        const lng = e.latlng.lng;

        placeMarker(lat, lng);

    });

    // ==========================================
    // CURRENT LOCATION
    // ==========================================

    const currentLocationBtn =
        document.getElementById("currentLocationBtn");

    if (currentLocationBtn) {

        currentLocationBtn.addEventListener(
            "click",

            function () {

                if (!navigator.geolocation) {

                    alert("Geolocation is not supported.");

                    return;

                }

                navigator.geolocation.getCurrentPosition(

                    function (position) {

                        const lat =
                            position.coords.latitude;

                        const lng =
                            position.coords.longitude;

                        map.setView(
                            [lat, lng],
                            16
                        );

                        placeMarker(
                            lat,
                            lng
                        );

                    },

                    function () {

                        alert(
                            "Unable to retrieve your location."
                        );

                    }

                );

            }

        );

    }

}
// ==========================================
// DELETE CONFIRMATION
// ==========================================

const deleteForms = document.querySelectorAll(".deleteForm");

deleteForms.forEach(form => {

    form.addEventListener("submit", function (e) {

        e.preventDefault();

        Swal.fire({

            title: "Delete Donation?",

            text: "This action cannot be undone.",

            icon: "warning",

            showCancelButton: true,

            confirmButtonColor: "#dc3545",

            cancelButtonColor: "#6c757d",

            confirmButtonText: "Yes, Delete",

            cancelButtonText: "Cancel"

        }).then((result) => {

            if (result.isConfirmed) {

                form.submit();

            }

        });

    });

});