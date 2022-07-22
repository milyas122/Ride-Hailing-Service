from . import response_builder
from marshmallow import ValidationError
from functools import wraps
from botocore.exceptions import ClientError
import json

def validate_body(Schema):
    @wraps(Schema)
    def decorator(func):
        def wrapper(event, context):
            try:
                if 'body' in event and event['body'] is not None:
                    data = json.loads(event['body'])
                else:
                    return response_builder.get_custom_error(status_code=400, message='Error',
                                                     data={'message': "Provide request body"})
                Schema.load(data)
                return func(event, context)
            except ClientError as e:
                return response_builder.get_custom_error(status_code=400, message='Error',
                                                         data={'message': e.response['Error']})
            except ValidationError as err:
                return response_builder.CustomValidationErrors(err).get_error()

        return wrapper

    return decorator