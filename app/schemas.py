from marshmallow import Schema, validate, fields


class PassesQuery(Schema):
    lat = fields.Float(required=True, validate=validate.Range(-90, 90))
    lon = fields.Float(required=True, validate=validate.Range(-180, 180))
    limit = fields.Int(missing=5, validate=validate.Range(1, 15))