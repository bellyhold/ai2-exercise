from dateutil.parser import isoparse
from marshmallow import ValidationError
from datetime import datetime, timezone
from pymongo import errors

from flask import jsonify

def handle_errors(error: Exception):

    # Handle duplicate key error
    if isinstance(error, errors.DuplicateKeyError):
        response = {
            "message": "Duplicate _id detected, unable to insert tip.",
        }
        return jsonify(response), 400

    # Handle generic errors
    response = {
        "message": "An unexpected error occurred",
        "error": str(error),
    }
    return jsonify(response), 500

def validate_date(value):
    try:
        iso_date = isoparse(value)
        if iso_date < datetime.now(timezone.utc):
            raise ValidationError("Tip has expired")
    except ValueError:
        raise ValidationError("Datetime needs to be in ISO format")