from marshmallow import Schema, validate, fields


class PassesQuery(Schema):
    lat = fields.Float(required=True, validate=validate.Range(-90, 90))
    lon = fields.Float(required=True, validate=validate.Range(-180, 180))
    limit = fields.Int(missing=100, validate=validate.Range(1, 100))
    days = fields.Int(missing=7, validate=validate.Range(1, 15))
    visible_only = fields.Boolean(missing=False)