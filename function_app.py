import azure.functions as func
import logging
import math
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="geoDistanceCalculator")
def geoDistanceCalculator(req: func.HttpRequest) -> func.HttpResponse:
    lat1 = req.params.get('lat1')
    long1 = req.params.get('long1')
    lat2 = req.params.get('lat2')
    long2 = req.params.get('long2')

    if lat1 == None or long1 == None or lat2 == None or long2 == None:
        return func.HttpResponse(json.dumps({'success': False, 'error': "Missing parameters"}), status_code=400)
    
    coord1 = (float(lat1), float(long1))
    coord2 = (float(lat2), float(long2))

    distance = haversine_distance(coord1, coord2)

    if distance == False:
        return func.HttpResponse(json.dumps({'success': False, 'error': "Invalid parameters"}), status_code=400)

    formattedDistance = formatOutput(distance)

    logging.info(f'({lat1},{long1}) -> ({lat2},{long2}) = {formattedDistance}')

    return func.HttpResponse(json.dumps({'success': True, 'distance': formattedDistance}), status_code=200)

def formatOutput(distance: float) -> str:
    if distance < 0:
        return False
    
    distance = int(distance)

    if distance == 0:
        return "0 m"
    
    digits = int(math.log10(distance))+1

    if digits <= 3:
        return f"{distance} m"
    else:
        distance /= 1000
        distance = int(distance)
        return f"{distance} km"

def haversine_distance(coord1: tuple, coord2: tuple) -> float:
    # Coordinates in decimal degrees
    lon1, lat1 = coord1
    lon2, lat2 = coord2

    R = 6371000  # radius of Earth in meters
    phi_1 = math.radians(lat1)
    phi_2 = math.radians(lat2)

    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi_1) * math.cos(phi_2) * math.sin(delta_lambda / 2.0) ** 2
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    d = R * c  # output distance in meters

    return d
