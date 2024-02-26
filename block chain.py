from flask import Flask, render_template, request, redirect
from flask import render_template_string
from datetime import datetime
import hashlib
import csv
import os

app = Flask(__name__)

# Password for accessing details
PASSWORD = "1168"  # Replace with your actual password
CSV_FILE_PATH = 'voting_data.csv'  # Replace with the actual absolute path

app = Flask(__name__, static_folder='static')


class VotingBlock:
    def __init__(self, index, timestamp, candidate_name, voter_id, previous_hash, hash=None):
        self.index = index
        self.timestamp = timestamp
        self.candidate_name = candidate_name
        self.voter_id = voter_id
        self.previous_hash = previous_hash
        self.hash = hash if hash else self.calculate_hash()

    def calculate_hash(self):
        hash_string = (
            str(self.index) +
            str(self.timestamp) +
            str(self.candidate_name) +
            str(self.voter_id) +
            str(self.previous_hash)
        )
        return hashlib.sha256(hash_string.encode()).hexdigest()

class VotingBlockchain:
    def __init__(self):
        self.chain = self.load_chain_from_csv()

    def load_chain_from_csv(self):
        if os.path.exists(CSV_FILE_PATH):
            with open(CSV_FILE_PATH, mode='r') as file:
                reader = csv.DictReader(file)
                return [VotingBlock(
                    int(row['Index']),
                    row['Timestamp'],
                    row['Candidate Name'],
                    row['Voter ID'],
                    row['Previous Hash'],
                    row['Hash']
                ) for row in reader]
        else:
            # If the file doesn't exist, create it with the genesis block
            return [self.create_genesis_block()]

    def save_chain_to_csv(self):
        with open(CSV_FILE_PATH, mode='w', newline='') as file:
            fieldnames = ['Index', 'Timestamp', 'Candidate Name', 'Voter ID', 'Previous Hash', 'Hash']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()
            for block in self.chain:
                writer.writerow({
                    'Index': block.index,
                    'Timestamp': block.timestamp,
                    'Candidate Name': block.candidate_name,
                    'Voter ID': block.voter_id,
                    'Previous Hash': block.previous_hash,
                    'Hash': block.hash
                })

    def create_genesis_block(self):
        return VotingBlock(0, datetime.now(), "Genesis Block", "Initial Voter ID", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, candidate_name, voter_id):
        # Check if the voter ID is numerical
        if not voter_id.isdigit():
            return False, "Voter ID must be in numerical format."

        # Check if the voter ID has already been used
        if any(block.voter_id == voter_id for block in self.chain):
            return False, "The voting is completed for this ID."

        new_block = VotingBlock(
            len(self.chain),
            datetime.now(),
            candidate_name,
            voter_id,
            self.get_latest_block().hash,
            ""  # Pass an empty string for the hash, as it will be calculated in the constructor
        )
        self.chain.append(new_block)
        self.save_chain_to_csv()
        return True, None

    def is_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

voting_blockchain = VotingBlockchain()

@app.route('/')
def index():
    return render_template('index.html', blockchain=voting_blockchain.chain)

@app.route('/add_block', methods=['GET', 'POST'])
def add_block():
    if request.method == 'POST':
        candidate_name = request.form['candidate_name']
        voter_id = request.form['voter_id']

        success, error_message = voting_blockchain.add_block(candidate_name, voter_id)
        if success:
            return redirect('/thanks_for_voting')  # Redirect to the thank you page
        else:
            candidates = get_candidate_names()
            return render_template('add_block.html', candidates=candidates, error_message=error_message)

    candidates = get_candidate_names()
    return render_template('add_block.html', candidates=candidates)

# Helper function to get the list of candidate names
def get_candidate_names():
    return ["Candidate 1", "Candidate 2", "Candidate 3","Candidate 4"]

@app.route('/thanks_for_voting')
def thanks_for_voting():
    return render_template('thanks_for_voting.html')

@app.route('/view_details', methods=['GET', 'POST'])
def view_details():
    if request.method == 'POST':
        entered_password = request.form['password']

        # Verify the password
        if entered_password == PASSWORD:
            return render_template('view_details.html', blockchain=voting_blockchain.chain)
        else:
            error_message = "Incorrect password. Please try again."
            return render_template('password_prompt.html', error_message=error_message)

    return render_template('password_prompt.html')

if __name__ == '__main__':
    app.run(debug=True)
