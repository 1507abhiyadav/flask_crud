import email
from email import message
import json
import jwt
import validators
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask import Flask,jsonify,request
from datetime import datetime, timedelta
from bson import encode, json_util, ObjectId
from pymongo import MongoClient
import pymongo
# expires= datetime.now() + timedelta(hours=24) -timedelta(hours=5)-timedelta(minutes=30)
app= Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)

try:
	client=pymongo.MongoClient('mongodb://localhost:27017/')
	print("Connected successfully!!!")
except:
	print("Could not connect to MongoDB")

mydb = client['employee']  # database name
collection = mydb['employee_1']  # collection name
collection_1 = mydb['employee_2']  # collection name


######## Register   using POST Method
@app.post('/register')
def user():
    username= request.json['username']
    email=request.json['email']
    password = request.json['password']
    args= request.json
    # print(args)
    if len(password)<8:
        return jsonify({"error":"Password is minimun 8 character"}),400
    if len(username)<3 :
        return jsonify({"error":"Invalid username"}),400
    if not validators.email(email):  ##  check Email valid or not by(validators)
        return jsonify({"error":"Invalid email"}),400

    try:
        all = collection.find_one({"email":args["email"]})
        pagae = json.loads(json_util.dumps(all))
        print(pagae)
        # return "created"
        if all == None:
            collection.insert_one(args)
            return jsonify({
                "status":"200",
                "massege":"Successfully register"
            }),200
        else:
            return jsonify({
                "status":"400",
                "massege":"email already exists"

            }),400
    except:
        return jsonify({
            "massege":"invalid"
        }),400


#######  Login  using POST Method

@app.post('/login')
def login():
    # username= request.json['username']
    email=request.json['email']
    password = request.json['password']
    args= request.json
    # print(args)
    if len(password)<8:
        return jsonify({"error":"Password is minimun 8 character"}),400
    # if len(username)<3 :
        # return jsonify({"error":"Invalid username"}),400
    if not validators.email(email):  ##  check Email valid or not by(validators)
        return jsonify({"error":"Invalid email"}),400

    try:
        all = collection.find_one({"email":args["email"],"password":args['password']})
        data = json.loads(json_util.dumps(all))
        print(data)
        # return "created"
        if all ==None:
            return jsonify({
                "status":"400",
                "message":"Email or Password invalid"
            }),400
        access_token = create_access_token(identity= data['email'])
        # print(access_token)
        return jsonify({
            "token": access_token,
            "status":200,
            "message":"Successfully login"
        }),200
    except Exception as e:
        return jsonify({
            "message":"error"+str(e)
        }),400


######## Get method

@app.get('/get')
@jwt_required()

def get():
    # return "suceessfully fetch data"
    all = collection_1.find()
    all_data = json.loads(json_util.dumps(all))
    # print(all_data)
    if all == None:
        return jsonify({
            "message":"[]"
        }),200
    else:
        return jsonify({ 
            "data":all_data
        }),200


##### POST Method

@app.post('/post')
@jwt_required()
def post():
    # username= request.json['username']
    # email=request.json['email']
    # password = request.json['password']
    # if len(password)<8:
    #     return jsonify({"error":"Password is minimun 8 character"}),400
    # if len(username)<3 :
    #     return jsonify({"error":"Invalid username"}),400
    # if not validators.email(email):  ##  check Email valid or not by(validators)
    #     return jsonify({"error":"Invalid email"}),400
    args= request.json
    # print(args)
    # return("successfully")
    try:

        all = collection_1.find_one({"email":args["email"]})
        all_data = json.loads(json_util.dumps(all))
        print(all_data)
        if all == None:
            collection_1.insert_one(args)
            return jsonify({
                "message":"successfully post"
            }),200
        else:
            return jsonify({
                "message":"email already exists"
            }),400 
    except Exception as e:
            return jsonify({
                "message":"error:"+str(e)
            }),400   


###### PUT Method

@app.put('/put')
@jwt_required()
def put():
    # username= request.json['username']
    # email=request.json['email']
    # password = request.json['password']

    # if len(password)<8:
    #     return jsonify({"error":"Password is minimun 8 character"}),400
    # if len(username)<3 :
    #     return jsonify({"error":"Invalid username"}),400
    # if not validators.email(email):   ##  check Email valid or not by(validators)
    #     return jsonify({"error":"Invalid email"}),400


    args = request.json
    # return ( "successfully update")
    try:
        all = collection_1.find_one({"email":args["email"]})
        all_data = json.loads(json_util.dumps(all))
        # print(all_data)
        if all == None:
            return jsonify({
                "message":"Email does not exists"
            }),400
        else:
            collection_1.update_one({'email':args['email']},{'$set':args})
            return jsonify({
                "message":" Data successfully update"
            }),200
    except Exception as e:
        return jsonify({
            "message":"error:"+str(e)
        }),400 


#####  DELETE Method

@app.delete('/delete')
@jwt_required()
def delete():
    # email=request.json['email']
    # args= request.json
    # # print(args)
    # if not validators.email(email):   ##  check Email valid or not by(validators)
    #     return jsonify({"error":"Invalid email"}),400
    # return ("delete")
    args = request.json
    try:
        all = collection_1.find_one({"email":args["email"]})
        all_data = json.loads(json_util.dumps(all))
        # print(all_data)
        if all == None:
            return jsonify({
                "message":"Email does not exists"
            }),400
        else:
            collection_1.delete_one(({'email':args['email']}))
            return  jsonify({
                "message":"Data Successfully Delete"
            }),200
    except Exception as e:
        return jsonify({
            "message":"error:"+str(e)
        }),400




if __name__ == '__main__':
    app.run(debug=True)