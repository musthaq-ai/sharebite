from flask import Blueprint, request, jsonify, current_app
import requests

location = Blueprint("location", __name__)


@location.route("/get-location", methods=["POST"])
def get_location():

    data = request.get_json()

    latitude = data.get("latitude")
    longitude = data.get("longitude")

    api_key = current_app.config["GOOGLE_MAPS_API_KEY"]

    url = (
        "https://maps.googleapis.com/maps/api/geocode/json"
        f"?latlng={latitude},{longitude}&key={api_key}"
    )

    response = requests.get(url)

    if response.status_code != 200:

        return jsonify({
            "success": False,
            "location": "Unknown"
        })

    result = response.json()

    if result["status"] != "OK":

        return jsonify({
            "success": False,
            "location": "Unknown"
        })

    address_components = result["results"][0]["address_components"]

    locality = None
    sublocality = None

    for component in address_components:

        types = component["types"]

        # City
        if "locality" in types:

            locality = component["long_name"]

        # Area / Neighbourhood
        elif "sublocality" in types or "sublocality_level_1" in types:

            sublocality = component["long_name"]

    # Prefer the area name
    if sublocality:

        location_name = sublocality

    elif locality:

        location_name = locality

    else:

        location_name = result["results"][0]["formatted_address"]

    return jsonify({

        "success": True,

        "location": location_name

    })