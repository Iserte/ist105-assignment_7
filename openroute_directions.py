import requests
import json

# === CONFIGURATION ===
DIRECTIONS_API = "https://api.openrouteservice.org/v2/directions/driving-car"
GEOCODE_API = "https://api.openrouteservice.org/geocode/search?"
API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjA2Y2ZjYmZkMTBkNjQwMDk4ZjFlMjhlOGFiMDg5ZDRlIiwiaCI6Im11cm11cjY0In0="

# === GEOCODING FUNCTION ===
def geocode_address(address):
    url = f"{GEOCODE_API}api_key={API_KEY}&text={address}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        json_data = response.json()
        if json_data["features"]:
            coords = json_data["features"][0]["geometry"]["coordinates"]
            if -90 <= coords[1] <= 90 and -180 <= coords[0] <= 180:
                return coords
            else:
                print(f"[Error] Invalid coordinates for '{address}'")
        else:
            print(f"[Error] No results found for '{address}'")
    except requests.exceptions.RequestException as e:
        print(f"[Network Error] {e}")
    return None

# === DIRECTIONS FUNCTION ===
def get_directions(orig_coords, dest_coords):
    body = { "coordinates": [orig_coords, dest_coords] }
    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(DIRECTIONS_API, headers=headers, json=body)
        response.raise_for_status()
        json_data = response.json()
        return json_data
    except requests.exceptions.RequestException as e:
        print(f"[Request Error] {e}")
    except json.JSONDecodeError:
        print("[Error] Failed to parse JSON response.")
    return None

# === DISPLAY FUNCTION ===
def display_trip_info(json_data, orig, dest):
    if 'routes' in json_data and json_data['routes']:
        route = json_data['routes'][0]
        if 'segments' in route and route['segments']:
            segment = route['segments'][0]
            duration_min = round(segment['duration'] / 60, 2)
            distance_km = round(segment['distance'] / 1000, 2)
            print("\n=============================================")
            print(f"Directions from {orig} to {dest}")
            print(f"Trip Duration: {duration_min} minutes")
            print(f"Distance: {distance_km} km")
            print("=============================================")
            if 'steps' in segment:
                for step in segment['steps']:
                    instruction = step.get('instruction', 'N/A')
                    step_distance = round(step.get('distance', 0) / 1000, 2)
                    print(f"- {instruction} ({step_distance} km)")
            else:
                print("No step-by-step directions available.")
            print("=============================================\n")
        else:
            print("[Error] No segments found in the route.")
    else:
        print("[Error] No routes found in the response.")

# === MAIN LOOP ===
while True:
    orig = input("Starting Location: ")
    if orig.lower() in ["quit", "q"]:
        break
    dest = input("Destination: ")
    if dest.lower() in ["quit", "q"]:
        break

    orig_coords = geocode_address(orig)
    dest_coords = geocode_address(dest)

    if not orig_coords or not dest_coords:
        print("[Error] Could not geocode one or both addresses. Please try again.\n")
        continue

    json_data = get_directions(orig_coords, dest_coords)
    if json_data:
        display_trip_info(json_data, orig, dest)