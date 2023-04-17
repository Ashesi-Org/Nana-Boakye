# this is the backend for the project 
from flask import Flask, jsonify, request
import json
import random
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


# service account configuration
cred = credentials.Certificate('web-tech-77405-firebase-adminsdk-vpgsu-0c9ae05cbc.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

# -------------- FIREBASE REFERENCES -----------------
userRef = db.collection('Users')
postRef = db.colllectioin('Posts')





app = Flask(__name__)

# create user code
# User Details needed:
# id, number, name, email, dob, year group, major, campus residence?, best food, best movie


@app.route('/Users', method=['POST'])
def createUser():
    userEmail = request.json['email']
    userAccount = userRef.doc(userEmail).get()
    newUser = {
        'userID': request.json['userID'],
        'phoneNumber': request.json['phoneNumber'],
        'email': request.json['email'],
        'dateOfBirth': request.json['dateOfBirth'],
        'yearGroup': request.json['yearGroup'],
        'campusResidence': request.json['campusResidence'],
        'favFood': request.json['favFood'],
        'favMovie': request.json['favMovie']
        
    }
    # check if user exists
    if userAccount.exists():
        return jsonify({'message':'User Already exists'}), 404


    # if user does not exist create new user
    try:
        userRef.doc(userEmail).set(newUser)
        return jsonify({'message': 'Successful', 'user': newUser }), 201

    except: 
        return jsonify({'message': 'Something went wrong'}), 404,



# Get user details 
@app.route('/Users', method=['GET'])
def getUserDetails():
    userEmail= request.json['email']

    # get user account and check whether it exists
    userAccount = userRef.doc(userEmail).get()
    if not userAccount.exists():
        return jsonify({'message':'Account does not exist'}), 404
    
    # if user exists return their details
    userInfo = userAccount.to_dict()
    return jsonify({'user':userInfo}), 201



# update user details
@app.route('/Users', method=['PUT'])
def updateUserDetails():
    userEmail = request.json['email']
    userAccount = userRef.doc(userEmail).get()
    
    # collect user data
    data = request.json

    # Update user in firestore 
    try : 
        userAccount.update(data)
        return jsonify({'Updated Successfully'}), 201

    except:
        return jsonify({'message':'An error occured during update'})


   
    # if user exists update details
    return 0

# delete user account
@app.route('/Users',method=['PUT'])
def deleteUserAccount():

#  Get user email to identify the document
    userEmail = request.json['email']
    userAccount = userRef.doc(userEmail).get()

# check if user exists
    if not userAccount.exists():
        return jsonify({'message': 'Something went wrong'}), 404

# delete user from firestore
    try: 
        userAccount.delete()
        return jsonify({'message':'Successfully Deleted'}), 201
    
    except: 
        return jsonify({'message': 'User could not be deleted'}), 404
    



# Create user post

# Get user posts

# delete user posg