from marshmallow import Schema, fields


class CreateTripSchema(Schema):
    destination = fields.String(required=True, error_messages={"required": "Destination is required field"})
    origin = fields.String(required=True, error_messages={"required": "Origin is required field"})
    total_distance = fields.String(required=True, error_messages={"required": "Total distance is required field"})
    duration = fields.String(required=True, error_messages={"required": "Duration is required field"})
    total_fare = fields.String(required=True, error_messages={"required": "Total fare is required field"})
 