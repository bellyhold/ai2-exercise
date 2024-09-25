#!/usr/bin/env python
import os

import requests
from apiflask import APIFlask
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.results import UpdateResult

from models import Tip, SatellitePartnerRequest
from utils import handle_errors
from uuid import uuid4

app = APIFlask(__name__)
app.config['VALIDATION_ERROR_STATUS_CODE'] = 400

@app.errorhandler(Exception)
def error_handler(error):
    return handle_errors(error)

client = MongoClient(os.environ['MONGODB_URI'])
tips: Collection


# POST /api/tip
# This endpoint receives a tip request from another service and should do the following:
# 1. Validate the request is valid.
# 2. Store the tip request into a data store.
# 3. Submit the tip request to the satellite-partner API. For the purposes of this exercise,
# you should POST the lat, lon, and expires_at fields to
# http://localhost:7200/api/task-satellite. The satellite-partner will
# respond with an HTTP 200 and a response body of {“tipIdentifier”:
# “abc123”}. This tipIdentifier is their unique id for this request and will be
# included in the callback. You do not need to write this other API service.
@app.post("/api/tip")
@app.input(Tip)  # The Schema for the Tip class handles validation in the models file
def process_tip(json_data):
    json_data["_id"] = json_data["event_id"]  # Use the event_id as the ObjectId in the mongo db.
    insert_result = tips.insert_one(document=json_data)
    # try:
    #     requests.post(os.environ['SATELLITE_PARTNER_API'], json=json_data)  # This will fail until implemented. Currently mocking response for testing purposes.
    # except Exception as e:
    #     raise e
    mocked_partner_response = {
        "tipIdentifier": str(uuid4())
    }
    # Update the existing record with the returned tipIdentifier
    tips.update_one({"_id": insert_result.inserted_id}, {"$set": mocked_partner_response})

    return mocked_partner_response, 200


# Receive Callback:
# POST /api/callback
# This endpoint is called by the satellite partner once our request has either been successfully
# fulfilled and imagery is available, or they were unable to fulfill the request. In practice, this
# callback might arrive hours or days later. On this request you should do the following:
# ● Update the tip record in your datastore with the provided data.
@app.post("/api/callback")
@app.input(SatellitePartnerRequest)  # The Schema for the SatellitePartnerRequest validation is also in the models file
def process_callback(json_data):
    result: UpdateResult = tips.update_one({"tipIdentifier": json_data["tipIdentifier"]}, {"$set": json_data})
    if result.matched_count < 1:
        raise Exception(f"Could not find tip with tipIdentifier: {json_data['tipIdentifier']}")
    return {}, 200


if __name__ == "__main__":
    print("Starting server...")
    with client.start_session(causal_consistency=True) as session:
        tips = client.db.tips
        app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT", 9090), debug=True)
