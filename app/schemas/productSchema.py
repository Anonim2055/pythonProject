from marshmallow import Schema, fields, validate

class ProductSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=2, max=30))
    description = fields.Str(required=False, validate=validate.Length(max=170))
    category = fields.Str(required=True, validate=validate.OneOf(["technologic", "home", "sport"]))
    price = fields.Float(required=True, validate=validate.Range(min=0))
    img_url = fields.Url(required=True)
