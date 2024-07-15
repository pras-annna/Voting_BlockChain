import cv2
import time
from pyzbar.pyzbar import decode
import hashlib
import pandas as pd

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "0", time.time(), "Genesis Block", self.calculate_hash(0, "0", time.time(), "Genesis Block"))

    def calculate_hash(self, index, previous_hash, timestamp, data):
        value = str(index) + previous_hash + str(timestamp) + data
        return hashlib.sha256(value.encode('utf-8')).hexdigest()

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        latest_block = self.get_latest_block()
        index = latest_block.index + 1
        timestamp = time.time()
        previous_hash = latest_block.hash
        hash = self.calculate_hash(index, previous_hash, timestamp, data)
        new_block = Block(index, previous_hash, timestamp, data, hash)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != self.calculate_hash(current_block.index, current_block.previous_hash, current_block.timestamp, current_block.data):
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

class Voter:
    def __init__(self, voter_id, public_key, name):
        self.voter_id = voter_id
        self.public_key = public_key
        self.name = name

class BlockchainVotingSystem:
    def __init__(self):
        self.blockchain = Blockchain()
        self.voters = {}  # Initialize an empty dictionary for voters
        self.voter_records = {}  # Dictionary to store voter records
        self.voted_voters = set()  # Set to keep track of voters who have already voted

    def load_voters_from_excel(self, file_path):
        try:
            df = pd.read_excel(file_path)
            for index, row in df.iterrows():
                voter_id = str(row['Voter ID'])  
                public_key = str(row['Public Key'])  
                name = str(row['Name'])  
                self.voters[voter_id] = Voter(voter_id, public_key, name)
                self.voter_records[voter_id] = {
                    'voter_id': voter_id,
                    'public_key': public_key,
                    'name': name,
                }
            print("Voters loaded successfully from Excel file.")
        except Exception as e:
            print(f"Error loading voters from Excel: {e}")

    def authenticate_voter(self):
        print("Scan your QR code to authenticate:")
        voter_id = scan_qr_code()
        if voter_id in self.voters:
            if voter_id not in self.voted_voters:
                voter_name = self.voters[voter_id].name
                print(f"Authentication successful!")
                print(f"Welcome, {voter_name}.")
                return voter_id
            else:
                print("This voter has already voted.")
                return None
        else:
            print("Authentication failed!")
            return None

    def cast_vote(self, voter_id, candidate):
        if voter_id:
            vote_data = f"Voter ID: {voter_id}, Candidate: {candidate}"
            self.blockchain.add_block(vote_data)
            self.voted_voters.add(voter_id)
            self.save_vote_to_excel(voter_id, candidate)
            print("Vote cast successfully!")
        else:
            print("Vote casting failed. Voter not authenticated or already voted.")

    def count_votes(self):
        results = {}
        for block in self.blockchain.chain[1:]:  
            data = block.data.split(", ")
            candidate = data[1].split(": ")[1]
            if candidate in results:
                results[candidate] += 1
            else:
                results[candidate] = 1
        return results

    def determine_winner(self):
        results = self.count_votes()
        if results:
            winner = max(results, key=results.get)
            return winner, results[winner]
        else:
            return None, 0

    def save_vote_to_excel(self, voter_id, candidate):
        vote_data = {
            'Index': len(self.blockchain.chain) - 1,
            'Voter ID': voter_id,
            'Candidate': candidate,
            'Timestamp': time.time(),
            'Previous Hash': self.blockchain.get_latest_block().previous_hash,
            'Hash': self.blockchain.get_latest_block().hash
        }
        df = pd.DataFrame([vote_data])
        try:
            with pd.ExcelWriter('votes.xlsx', mode='a', if_sheet_exists='overlay', engine='openpyxl') as writer:
                startrow = writer.sheets['Sheet1'].max_row
                df.to_excel(writer, startrow=startrow, index=False, header=False)
        except FileNotFoundError:
            df.to_excel('votes.xlsx', index=False)

    def save_winner_to_excel(self, winner, votes):
        winner_data = {
            'Index': len(self.blockchain.chain),
            'Voter ID': 'Winner',
            'Candidate': winner,
            'Votes': votes,
            'Timestamp': time.time(),
            'Previous Hash': self.blockchain.get_latest_block().hash,
            'Hash': self.blockchain.calculate_hash(len(self.blockchain.chain), self.blockchain.get_latest_block().hash, time.time(), winner)
        }
        df = pd.DataFrame([winner_data])
        try:
            with pd.ExcelWriter('votes.xlsx', mode='a', if_sheet_exists='overlay', engine='openpyxl') as writer:
                startrow = writer.sheets['Sheet1'].max_row
                df.to_excel(writer, startrow=startrow, index=False, header=False)
        except FileNotFoundError:
            df.to_excel('votes.xlsx', index=False)

# Function to scan QR code
def scan_qr_code():
    cap = cv2.VideoCapture(0)
    while True:
        _, frame = cap.read()
        decoded_objects = decode(frame)
        for obj in decoded_objects:
            qr_data = obj.data.decode('utf-8')
            print(f"QR Code Data: {qr_data}")
            cap.release()
            cv2.destroyAllWindows()
            return qr_data
        cv2.imshow("QR Code Scanner", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    voting_system = BlockchainVotingSystem()
    voting_system.load_voters_from_excel('voter.xlsx')

    print("Current Voter Records:")
    for voter_id, record in voting_system.voter_records.items():
        print(f"Voter ID: {voter_id}")
        print(f"Name: {record['name']}")
        print()

    num_voters = int(input("Enter the number of voters: "))

    for _ in range(num_voters):
        print(f"Voter {_ + 1}:")
        voter_id = voting_system.authenticate_voter()
        if voter_id:
            candidate = input("Enter the candidate name (e.g., Candidate A): ")
            voting_system.cast_vote(voter_id, candidate)
            print()

    print("Current vote count:", voting_system.count_votes())

    winner, votes = voting_system.determine_winner()
    if winner:
        print(f"The winner is {winner} with {votes} votes.")
        voting_system.save_winner_to_excel(winner, votes)
    else:
        print("No votes cast.")
