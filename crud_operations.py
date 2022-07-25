from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    unset_jwt_cookies,
    jwt_required,
    JWTManager,
)
import pymongo
from pymongo import MongoClient
from bson.json_util import dumps
import os


DB_HOST = os.environ.get("DB_HOST")
client = pymongo.MongoClient(DB_HOST)


crud_operations_blueprint = Blueprint("crud_operations_blueprint", __name__)

@crud_operations_blueprint.route("/images", methods=["GET", "POST", "DELETE"])
@jwt_required()

def images():

    if request.method == "GET":
        db = client["images-db"]
        usersCollection = db["users"]
        identity = get_jwt_identity()
        userImages = dumps(usersCollection.find({"email": identity}, {"images": 1, "_id": 0} ))
        return userImages

    if request.method == "POST":
        db = client["images-db"]
        usersCollection = db["users"]
        identity = get_jwt_identity()
        alreadySaved = False
        img = request.get_json()
        imgId = img['id']
        userImages = list(usersCollection.find({'$and': [ {"email":identity}, {"images.id": imgId} ]}, {"images.id":1}))
        if (len(userImages) == 0):
            usersCollection.update_one({"email": identity}, { "$push": {'images': img} })
            alreadySaved = "False"
            return alreadySaved, 201
        if (len(userImages)>0):
            alreadySaved = "True"
            return alreadySaved, 202

    if request.method == "DELETE":
        db = client["images-db"]
        usersCollection = db["users"]
        identity = get_jwt_identity()
        img = request.get_json()
        usersCollection.update_one({"email": identity}, { "$pull": {'images': img} })
        return "Image Deleted"
