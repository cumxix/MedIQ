import requests


def find_nearby_pharmacies(latitude, longitude):

    query = f"""
    [out:json];
    (
      node
        ["amenity"="pharmacy"]
        (around:3000,{latitude},{longitude});
    );
    out;
    """

    url = "https://overpass-api.de/api/interpreter"

    response = requests.get(
        url,
        params={"data": query},
        timeout=20
    )

    if response.status_code != 200:
        return []

    data = response.json()

    pharmacies = []

    for item in data.get("elements", [])[:5]:

        name = item.get("tags", {}).get("name", "Unknown Pharmacy")

        lat = item["lat"]
        lon = item["lon"]

        link = f"https://maps.google.com/?q={lat},{lon}"

        pharmacies.append({
            "name": name,
            "link": link
        })

    return pharmacies