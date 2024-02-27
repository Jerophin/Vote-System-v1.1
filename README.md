# Voting Blockchain Application
This is a simple blockchain-based voting application built using Flask, allowing users to cast votes for different candidates. The application utilizes a blockchain to store and secure voting data. Below is an overview of the files and functionalities:

## Files:
app.py: This is the main Python file that contains the Flask application. It defines routes, handles form submissions, and interacts with the blockchain.

templates/: This directory contains HTML templates for different pages in the application.

static/: This directory holds static files such as stylesheets or images.

voting_data.csv: A CSV file used as a data storage mechanism for the blockchain. It contains information about each block in the chain.

## Features:

### Blockchain Implementation:

The application uses a simple blockchain structure to store and validate votes.
Each block in the blockchain contains information such as index, timestamp, candidate name, voter ID, previous hash, and hash.

### Genesis Block:
The blockchain starts with a genesis block containing initial data.

### Voting:
Users can cast votes for candidates by providing their names and voter IDs.
The application ensures that each voter can vote only once.

### Password Protection:
Access to view the voting details is protected by a password (PASSWORD in the code).
Users need to enter the correct password to view the voting details.

### Data Persistence:
The blockchain data is stored in a CSV file (voting_data.csv), allowing data to persist between application runs.
Validation:

### The application performs basic validation, such as checking if the voter ID is numerical and if it has already been used for voting.

## How to Run:

### Clone the repository:

Copy code

git clone https://github.com/your-username/voting-system-v1.1.git

### Install dependencies:

Copy code:

pip install -r requirements.txt

### Run the application:

Copy code

python block chain.py

Access the application in your browser at http://localhost:5000.

## Note:
Ensure that you replace the placeholder values such as PASSWORD and CSV_FILE_PATH with your actual password and file paths in the code.

This application is meant for educational purposes and may require additional security measures for production use.

Feel free to explore and modify the code according to your needs. If you have any questions or suggestions, please don't hesitate to reach out. Happy voting! 🗳️🔒
