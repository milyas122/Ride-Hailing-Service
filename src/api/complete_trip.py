import json
import os 
import boto3
from botocore.exceptions import ClientError
from ..common import utils
from ..common.response_builder import (
    get_success_response, get_custom_error
)

dynamodb = boto3.resource('dynamodb')
TRIP_TABLE = os.environ['TRIP_TABLE'] # Table Name 
trip_table = dynamodb.Table(TRIP_TABLE) # Dynamodb Table 

def lambda_handler(event, context):
    try:
        
        trip_id = event["pathParameters"]["tripId"]

        
        # Ensure Trip exist in DB or not
        trip_record = trip_table.get_item(
            Key = {
                "Pk":trip_id
            }
        )
        
        if not trip_record.get("Item"):
            raise ValueError("Invalid Trip Id")
        
        now = utils.utc_now

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
    
    except Exception as e:
        return get_custom_error(status_code=400, message="Bad Request", data={"message":"Something went wrong, come back later"})
       


    
