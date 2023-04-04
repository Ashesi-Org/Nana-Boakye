from flask import Flask, jsonify, request
import random
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


# service account configuration
cred = credentials.Certificate('web-tech-77405-firebase-adminsdk-vpgsu-0c9ae05cbc.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

app = Flask(__name__)


voter_ref = db.collection('voters')
vote_cast_ref = db.collection('votes')
election_ref = db.collection('elections')


# Register a voter
@app.route('/voters', methods=['POST'])
def register_voter():
    user_id = str(random.randint(0,10))
    voter = {
        'id': user_id,
        'name': request.json['name'],
        'email': request.json['email'],
        'student_id': request.json['student_id'],
        'year_group': request.json['year_group'],
        'major': request.json['major']
    }
    # check whether collection exists
    # if it does return client exists
    # if it doesnt put in datastore

    
    voter_ref.document(user_id).set(voter)
    return jsonify({'message': 'Voter registration successful', 'voter': voter}), 201
@app.route('/')
def main():
    return 'Hello World'


# De-register a voter
@app.route('/voters/<int:voter_id>', methods=['DELETE'])
def deregister_voter(voter_id):
    voter = str(voter_id)
    if not voter_ref.document(voter).get().exists:
        return jsonify({'error': 'user not found'}), 404

    # Delete user   
    voter_ref.document(voter).delete()
    return jsonify({'message': 'Voter de-registration successful'})
   

# Update a voter's information
@app.route('/voters/<int:voter_id>', methods=['PUT'])
def update_voter(voter_id):
    voter = str(voter_id)

    # collect the data
    data = request.json

    if not voter_ref.document(voter).get().exists:
        return jsonify({'error': 'user not found'}), 404

    # Update user   
    voter_ref.document(voter).update(data)
    return jsonify({'message': 'Voter update successful'}), 200
   


# Retrieve a voter
@app.route('/voters/<int:voter_id>', methods=['GET'])
def get_voter(voter_id):
    print(voter_id)
    voter = str(voter_id)

    if not voter_ref.document(voter).get().exists:
        return jsonify({'error': 'user not found'}), 404
    
    voter_information = voter_ref.document(voter).get().to_dict()

    return jsonify({'voter': voter_information}), 404

# Create an election
@app.route('/elections', methods=['POST'])
def create_election():
    election_id = str(random.randint(0,5))
    election = {
        'id': election_id,
        'name': request.json['name'],
        'start_date': request.json['start_date'],
        'end_date': request.json['end_date'],
        'candidates': request.json['candidates']
    }
    
       
    election_ref.document(election_id).set(election)
    return jsonify({'message': 'Election registration successful', 'election': election}), 201




# Retrieve an election
@app.route('/elections/<int:election_id>', methods=['GET'])
def get_election(election_id):
    # with open('./tmp/election.txt', 'r') as f:
    #     data = f.read()
    #     elections = json.loads(data)

    #     for election in elections:
    #         if election['id'] == election_id:
    #             return jsonify({'election': election}), 200
    election = str(election_id)
    if not election_ref.document(election).get().exists:
        return jsonify({'error': 'user not found'}), 404
    
    election_info = election_ref.document(election).get().to_dict()
    return jsonify({'election': election_info}), 404

# Delete an election
@app.route('/elections/<int:election_id>', methods=['DELETE'])
def delete_election(election_id):
    elections =str(election_id)
    
    if not voter_ref.document(elections).get().exists:
        return jsonify({'error': 'user not found'}), 404
    
    election_ref.document(elections).delete()
    return jsonify({'message': 'Election deleted'}), 200

# Vote in an election
@app.route('/elections/<int:election_id>/votes', methods = ['POST'])
def vote_election():
    student_vote = {
        'election_id': request.json['election_id'],
        'voter_id': request.json['voter_id'],
        'candidate_id': request.json['candidate_id'],
    }
    vote_cast_ref.document().set(student_vote)

    return jsonify({'voter': student_vote}), 201


if __name__ == '__main__':
    app.run()