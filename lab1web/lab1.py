from flask import Flask, jsonify, request
import json
import random

app = Flask(__name__)

voters = []
elections = []

# Register a voter
@app.route('/voters', methods=['POST'])
def register_voter():
    voter = {
        'id': random.randint(0,5),
        'name': request.json['name'],
        'email': request.json['email'],
        'student_id': request.json['student_id'],
        'year_group': request.json['year_group'],
        'major': request.json['major']
    }
    with open('./tmp/voter.txt', 'r') as f:
        data = f.read()
    if not data:
        records = [voter]
    else:
        records = json.loads(data)
        records.append(voter)
    with open('./tmp/voter.txt', 'w') as f:
        f.write(json.dumps(records, indent=2))
    return jsonify({'message': 'Voter registration successful', 'voter': voter}), 201

# De-register a voter
@app.route('/voters/<int:voter_id>', methods=['DELETE'])
def deregister_voter(voter_id):
    new_voters = []
    with open('./tmp/voter.txt', 'r') as f:
        data = f.read()
        voters = json.loads(data)
        for voter in voters:
            if voter['id'] == voter_id:
                continue
            new_voters.append(voter)
    with open('./tmp/voter.txt', 'w') as f:
        f.write(json.dumps(new_voters, indent=2))  
    return jsonify({'message': 'Voter de-registration successful'})
   

# Update a voter's information
@app.route('/voters/<int:voter_id>', methods=['PUT'])
def update_voter(voter_id):
    new_records = []
    with open('./tmp/voter.txt', 'r') as f:
        data = f.read()
        voters = json.loads(data)
    for voter in voters:
        if voter['id'] == voter_id:
            voter['name'] = request.json.get('name', voter['name'])
            voter['email'] = request.json.get('email', voter['email'])
            voter['student_id'] = request.json.get('student_id', voter['student_id'])
            voter['year_group'] = request.json.get('year_group', voter['year_group'])
            voter['major'] = request.json.get('major', voter['major'])
            return jsonify({'message': 'Voter information updated', 'voter': voter}), 200
        new_records.append(voter)
    with open('./tmp/voter.txt', 'w') as f:
        f.write(json.dumps(new_records, indent=2))
    return jsonify({'message': 'Voter not found'}), 404

# Retrieve a voter
@app.route('/voters/<int:voter_id>', methods=['GET'])
def get_voter(voter_id):
    print(voter_id)
    with open('./tmp/voter.txt', 'r') as f:
        data = f.read()
        voters = json.loads(data)
        for voter in voters:
            if voter['id'] == voter_id:
                return jsonify({'voter': voter}), 200
        return jsonify({'message': 'Voter not found'}), 404

# Create an election
@app.route('/elections', methods=['POST'])
def create_election():
    election = {
        'id': random.randint(0,5),
        'name': request.json['name'],
        'start_date': request.json['start_date'],
        'end_date': request.json['end_date'],
        'candidates': request.json['candidates']
    }
    with open('./tmp/election.txt', 'r') as f:
        data = f.read()
    if not data:
        records = [election]
    else:
        records = json.loads(data)
        records.append(election)
    with open('./tmp/election.txt', 'w') as f:
        f.write(json.dumps(records, indent=2))

    return jsonify({'message': 'Election created', 'election': election}), 201

# Retrieve an election
@app.route('/elections/<int:election_id>', methods=['GET'])
def get_election(election_id):
    with open('./tmp/election.txt', 'r') as f:
        data = f.read()
        elections = json.loads(data)

        for election in elections:
            if election['id'] == election_id:
                return jsonify({'election': election}), 200
        return jsonify({'message': 'Election not found'}), 404

# Delete an election
@app.route('/elections/<int:election_id>', methods=['DELETE'])
def delete_election(election_id):
    new_elections = []
    with open('./tmp/data.txt', 'r') as f:
        data = f.read()
        elections = json.loads(data)
        for election in elections:
            if election['id'] == election_id:
                continue
            new_elections.append(election)
    with open('./tmp/election.txt', 'w') as f:
        f.write(json.dumps(new_elections, indent=2))
            
    return jsonify({'message': 'Election deleted'}), 200

# Vote in an election
@app.route('/elections/<int:election_id>/votes', methods = ['POST'])
def vote_election():
    student_vote = {
        'voter_id': request.json['voter_id'],
        'candidate_id': request.json['candidate_id'],
    }
    with open('./tmp/election_votes.txt', 'r') as f:
        data = f.read()
    if not data:
        records = [student_vote]
    else:
        records = json.loads(data)
        records.append(student_vote)
    with open('./tmp/election_votes.txt', 'w') as f:
        f.write(json.dumps(records, indent=2))
    return jsonify({'message': 'Student successfully voted', 'voter': student_vote}), 201


if __name__ == '__main__':
    app.run()
