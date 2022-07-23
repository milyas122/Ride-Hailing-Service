import os 
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
from ..common.response_builder import (
    get_success_response, get_custom_error
)

dynamodb = boto3.resource('dynamodb')
TRIP_TABLE = os.environ['TRIP_TABLE'] # Table Name 
trip_table = dynamodb.Table(TRIP_TABLE) # Dynamodb Table 

def lambda_handler(event, context):
    try:
        
        # All Completed Trips Will be get from DB
        trip_record = trip_table.query(
            IndexName='status-date-index',
            KeyConditionExpression=Key('status').eq("completed")
        )["Items"]
        
        if not trip_record:
            return get_success_response(status_code=200, message='Success', data={"message": "No records found..."})
      
        return get_success_response(status_code=200, message='Success', data={"Items": trip_record})

    except ClientError as e:
        return get_custom_error(status_code=500, message='Server Error', data={"message":e.response['Error']})
    
    except ValueError as e:
        return get_custom_error(status_code=400, message='Bad Request', data={"message":str(e)})
       


    
