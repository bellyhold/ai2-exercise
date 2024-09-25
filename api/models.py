
from apiflask import Schema
from apiflask.fields import String, Float

from utils import validate_date


class Tip(Schema):
    lat = Float(required=True)
    lon = Float(required=True)
    expires_at = String(required=True, validate=validate_date)
    event_id = String(required=True)

class SatellitePartnerRequest(Schema):
    tipIdentifier = String(required=True)
    status = String(required=True)
    imageLocation = String(required=False)
    collectedAt = String(required=False, validate=validate_date)