from marshmallow import Schema,fields,validate


class UserSchema(Schema):
    name= fields.Str(required=True,validate=validate.Length(min=2, max=30))
    email = fields.Email(required=True, validate=validate.Length(min=4, max=30))
    password = fields.Str(required=True, validate=validate.Length(min=6, max=50))

class UserUpdateSchema(Schema):
    name = fields.Str(validate=validate.Length(min=2, max=30))
    email = fields.Email(validate=validate.Length(min=4, max=30))
    password = fields.Str(validate=validate.Length(min=6, max=50))

class LoginSchema(Schema):
    email = fields.Email(required=True, validate=validate.Length(min=4, max=30))
    password = fields.Str(required=True, validate=validate.Length(min=6, max=50))



    # ? Marshmallow provides a broad range of functionalities for validating and deserializing input data, as well as serializing objects or complex data types to simple types. Here are some examples of what you can do with Marshmallow:

    # TODO: Fields:

    # ? Str(): String field, optionally strip whitespace.
    # ? Bool(): Boolean field.
    # ? Int(): Integer field.
    # ? Float(): Float field.
    # ? DateTime(): DateTime field.
    # ? Email(): Email field, applies an email validation.
    # ? Url(): URL field, applies URL validation.
    # ? List(): List field, takes another field as its argument.
    # ? Nested(): Nested field, takes a schema as its argument.
    # ? Dict(): Dictionary field.
    # ? Method(): Custom method field.
    # ? Function(): Custom function field.
    # ? Pluck(): Takes a field name to pluck from an object and an attribute name to store the result.

    # TODO: Validation:
    # ? required: Makes the field required.

    # ? validate.Length(min=, max=): Validates the length of a string.

    # ? validate.Range(min=, max=): Validates the range of a number.

    # ? validate.OneOf(choices=): Validates that the value is one of the provided choices.

    # ? validate.NoneOf(choices=): Validates that the value is not one of the provided choices.

    # ? validate.Regexp(regex=): Validates the value against a regular expression.

    # ? validate.Email(): Validates the value as an email.

    # ? validate.URL(): Validates the value as a URL.

    # ? validate.Predicate(predicate=): Custom validation using a predicate function.

    # ? validate.ContainsOnly(choices=): Validates that a list contains only the provided choices.

    # ? Example:
    # class UserSchema(Schema):
    #     name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    #     email = fields.Email(required=True)
    #     password = fields.Str(required=True, validate=validate.Length(min=6))
    #     age = fields.Int(required=True, validate=validate.Range(min=18))
    #     hobbies = fields.List(fields.Str(), validate=validate.Length(max=10))
    #     favorite_color = fields.Str(validate=validate.OneOf(choices=['red', 'green', 'blue']))
    #     website = fields.Url()
