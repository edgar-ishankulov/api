from flask import Blueprint, jsonify, request
import os
import requests
UNSPLASH_URL = "https://api.unsplash.com/photos/random/"
from bson.json_util import dumps

UNSPLASH_KEY = os.environ.get("UNSPLASH_KEY", "")
new_image_blueprint = Blueprint("new_image", __name__)

@new_image_blueprint.route("/new-image")
def new_image():
    word = request.args.get("query")
    headers = {"Authorization": "Client-ID " + UNSPLASH_KEY, "Accept-Version": "v1"}
    params = {"query": word, "count": 30}
    response = requests.get(url=UNSPLASH_URL, headers=headers, params=params)
    data = response.json()
    resultsArray = list(data)
    print(resultsArray)
    print(len(resultsArray))
    if len(resultsArray) < 2:
        return 'No valid results', 400
    return dumps(data), 200