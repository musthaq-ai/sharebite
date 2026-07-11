
let currentMap;
let currentMarker;

document.addEventListener("DOMContentLoaded", () => {

    if (!navigator.geolocation) {

        Swal.fire({

            icon: "error",

            title: "GPS Not Supported",

            text: "Your browser does not support GPS."

        });

        return;
    }

    navigator.geolocation.getCurrentPosition(

        showLocation,

        showError,

        {

            enableHighAccuracy: true

        }

    );

});

function showLocation(position) {

    const latitude = position.coords.latitude;

    const longitude = position.coords.longitude;

    currentMap = L.map("currentLocationMap").setView(

        [latitude, longitude],

        16

    );

    L.tileLayer(

        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",

        {

            attribution:

                "&copy; OpenStreetMap Contributors"

        }

    ).addTo(currentMap);

    currentMarker = L.marker(

        [latitude, longitude]

    ).addTo(currentMap);

    currentMarker.bindPopup(

        "<b>You are here 📍</b>"

    ).openPopup();

}
function showError(error){

    let message="Unable to detect location.";

    switch(error.code){

        case error.PERMISSION_DENIED:

            message="Location permission denied.";

            break;

        case error.POSITION_UNAVAILABLE:

            message="Location unavailable.";

            break;

        case error.TIMEOUT:

            message="Location request timed out.";

            break;
    }

    Swal.fire({

        icon:"warning",

        title:"GPS",

        text:message

    });

}