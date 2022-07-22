import json
import os 
import boto3
import uuid
import pytz
from datetime import datetime
from botocore.exceptions import ClientError
from ..validations.create_trip import CreateTripSchema
from ..common.decoartors import validate_body
from ..common.response_builder import (
    get_success_response, get_custom_error
)

dynamodb = boto3.resource('dynamodb')
TRIP_TABLE = os.environ['TRIP_TABLE'] # Table Name 
trip_table = dynamodb.Table(TRIP_TABLE) # Dynamodb Table 

tz_PAK = pytz.timezone('Asia/Karachi')

@validate_body(CreateTripSchema())
def lambda_handler(event, context):
    try:
        data = json.loads(event["body"])

        destination =  data["destination"]
        origin = data["origin"]
        total_distance = data["total_distance"]
        duration = data["duration"]
        total_fare = data["total_fare"]

        datetime_PAK = datetime.now(tz_PAK)
        now = datetime_PAK.strftime("%Y-%m-%dT%H:%M:%S")
        trip_id = str(uuid.uuid4())
        
        trip_table.put_item(
            Item = {
                "Pk": trip_id,
                "created_at": now,
                "destination": destination,
                "origin": origin,
                "total_duration": duration,
                "total_distance_traveled":total_distance,
                "total_fare": total_fare
            }
        )

        return get_success_response(status_code=201, message='Success', data={"message": "Trip created successfully.."})

    except ClientError as e:
        return get_custom_error(status_code=500, message='Server Error', data={"message":e.response['Error']})

    except ValueError as e:
        return get_custom_error(status_code=400, message='Bad Request', data={"message":str(e)})
       


    
