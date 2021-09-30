from marshmallow import Schema, fields, validate


class UserUrlParamsSchema(Schema):
    user_id = fields.Int(required=True)


class SaveNewUserSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(max=128))
    x = fields.Decimal(required=True)
    y = fields.Decimal(required=True)


class UserNeighborsSchema(Schema):
    user_id = fields.Int(required=True)
    radius = fields.Decimal(required=True)
    limit = fields.Int(required=True)
