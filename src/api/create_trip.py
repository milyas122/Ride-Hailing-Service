import json
import os 
import boto3
import uuid
from botocore.exceptions import ClientError
from ..validations.create_trip import CreateTripSchema
from ..common import utils
from ..common.decoartors import validate_body
from ..common.response_builder import (
    get_success_response, get_custom_error
)

dynamodb = boto3.resource('dynamodb')
TRIP_TABLE = os.environ['TRIP_TABLE'] # Table Name 
trip_table = dynamodb.Table(TRIP_TABLE) # Dynamodb Table 


@validate_body(CreateTripSchema())
def lambda_handler(event, context):
    try:
        data = json.loads(event["body"])

        destination =  data["destination"]
        origin = data["origin"]
        total_distance = data["total_distance"]
        duration = data["duration"]
        total_fare = data["total_fare"]

        now = utils.utc_now
        
        trip_id = str(uuid.uuid4())
        data = {
                "Pk": trip_id,
                "created_at": now,
                "destination": destination,
                "origin": origin,
                "total_duration": duration,
                "total_distance_traveled":total_distance,
                "total_fare": total_fare,
                "status":"pending"
            }
        trip_table.put_item(
            Item = data
        )

        return get_success_response(status_code=201, message='Success', data={"message": "Trip created successfully..","data":data})

    except ClientError as e:
        return get_custom_error(status_code=500, message='Server Error', data={"message":e.response['Error']})

    except Exception as e:
        return get_custom_error(status_code=400, message="Bad Request", data={"message":"Something went wrong, come back later"})


    
