from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps

# This is a function that returns a decorator. It requires a 'role' parameter.
def role_required(role):
    # This is the decorator function. It takes a function 'func' as parameter.
    def decorator(func):
        # 'wraps' is a decorator factory that applies the 'update_wrapper()' function
        # to the decorated function. It helps to keep the metadata of the decorated function.
        @wraps(func)
        # jwt_required is a decorator to protect endpoints. It checks if the request contains
        # a valid JWT token.
        @jwt_required()
        # This is the new function that the decorator returns. It will replace the decorated function.
        # It takes any positional and keyword arguments, which allows it to replace any function.
        def wrapper(*args, **kwargs):
            # Get the identity of the JWT. The identity can be any data that is json serializable.
            # In your case, it's probably a dictionary containing information about the user.
            payload = get_jwt_identity()
            if payload['role'] == 'admin':
                # next to route
                return func(*args, **kwargs)
            # Check if the role in the JWT payload matches the required role.
            if payload['role'] != role:
                # If roles don't match, return an error response.
                return jsonify({"error": "Unauthorized access"}), 403
            else:
                # If roles match, call the decorated function and return its result.
                return func(*args, **kwargs)
        # The decorator returns the new function.
        return wrapper
    # The role_required function returns the decorator.
    return decorator