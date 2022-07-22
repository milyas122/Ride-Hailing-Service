import json
import requests
import os 

def lambda_handler(event, context):
    try:
        api_key = os.environ["API_KEY"]

        # For demo purposes we use hardcoded trip_fare.
        # But in poroduction trip_fare actually get from database
        per_hunder_meter_fare: float = 2.0 # per 1000meter/1km fare
        per_meter_fare: float = per_hunder_meter_fare/1000 # per 1 meter fare

        url_query_params = event.get("queryStringParameters")
        
        if not url_query_params or not url_query_params.get("origins") or not url_query_params.get("destinations"):
            raise ValueError("Provide both origin/destination for trip")
        
        origins = url_query_params["origins"]
        destinations = url_query_params["destinations"]

        # Google Distance Matrix Api call 
        url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origins}&destinations={destinations}&key={api_key}"
        payload = {}
        headers = {}
        api_response = requests.request("GET", url, headers=headers, data=payload)
        result = api_response.json()

        data:dict = {}
        if result["status"] == "OK":

            elements: dict = result["rows"][0]["elements"][0]
            
            if elements["status"] != "OK":
                raise ValueError("Make sure your search is spelled correctly. Try adding a city,state, or zip code")

            total_fare:float = per_meter_fare * elements["distance"]["value"]
            data = {
                "destination": result["destination_addresses"][0],
                "origin": result["origin_addresses"][0],
                "total_distance": elements["distance"]["text"],
                "duration": elements["duration"]["text"],
                "total_fare": f"{total_fare} $"
            }
        else:
            raise ValueError("Something went wrong, come back later")

        response = {
            "statusCode": 200,
            "body": json.dumps({
                'responseCode': 200,
                'message': "Success",
                'response': data
            })
        }

        return response
    except ValueError as e:
        return {
            "statusCode": 400,
            "body": json.dumps({
                'responseCode': 200,
                'message': "Bad Request",
                'response': {"message":str(e)}
            })
        }


    
