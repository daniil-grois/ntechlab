from marshmallow import Schema, fields, validate


class UserUrlParamsSchema(Schema):
    user_id = fields.Int(required=True)


class SaveNewUserSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(max=128))
    x = fields.Float(required=True)
    y = fields.Float(required=True)


class UserNeighborsSchema(Schema):
    user_id = fields.Int(required=True)
    radius = fields.Float(required=True)
    limit = fields.Int(required=True)
