import json
import os 
import boto3
import uuid
import pytz
from datetime import datetime
from botocore.exceptions import ClientError
from ..common.response_builder import (
    get_success_response, get_custom_error
)

dynamodb = boto3.resource('dynamodb')
TRIP_TABLE = os.environ['TRIP_TABLE'] # Table Name 
trip_table = dynamodb.Table(TRIP_TABLE) # Dynamodb Table 

tz_PAK = pytz.timezone('Asia/Karachi')

def lambda_handler(event, context):
    try:
        
        trip_id = event["pathParameters"]["tripId"]

        datetime_PAK = datetime.now(tz_PAK)
        now = datetime_PAK.strftime("%Y-%m-%dT%H:%M:%S")
        
        # Ensure Trip exit in DB or not
        trip_record = trip_table.get_item(
            Key = {
                "Pk":trip_id
            }
        )
        
        if not trip_record.get("Item"):
            raise ValueError("Invalid Trip Id")

        # Mark trip to completed 
        trip_table.update_item(
            Key = {
                "Pk": trip_id
            },
            UpdateExpression = "SET #st = :v1, updated_at = :v2",
            ExpressionAttributeValues = {
                ":v1": "completed",
                ":v2": now
            },
            ExpressionAttributeNames = {
                "#st": "status"
            }
        )

      
        return get_success_response(status_code=201, message='Success', data={"message": "Trip complete successfully.."})

    except ClientError as e:
        return get_custom_error(status_code=500, message='Server Error', data={"message":e.response['Error']})
    
    except ValueError as e:
        return get_custom_error(status_code=400, message='Bad Request', data={"message":str(e)})
       


    
