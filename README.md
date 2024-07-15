Welcome to the Secure Voting with BlockChain ! This is Collaborative project done within 12hr as team with Srinivasan[https://github.com/Srini-23] and Dharshna[https://github.com/Dharshna2805]

Blockchain-Based Voting System
Overview
This project demonstrates the implementation of a blockchain-based voting system. It leverages the immutability and transparency of blockchain technology to ensure the integrity of the voting process. Additionally, it includes voter authentication using QR codes, ensuring that only registered voters can cast their votes.

Features
Blockchain Implementation: The voting system uses a simple blockchain to record votes. Each vote is stored as a block, ensuring immutability and transparency.
QR Code Authentication: Voters are authenticated using QR codes, which are scanned to verify their identity.
Excel Integration: Voter records are loaded from an Excel file, and votes are saved back to Excel for persistent storage and analysis.
Vote Counting and Winner Determination: The system can count votes and determine the winner of the election.
Project Structure
Classes and Functions
Block Class: Represents a block in the blockchain.
Blockchain Class: Manages the chain of blocks, including block creation and validation.
Voter Class: Represents a voter with a unique ID, public key, and name.
BlockchainVotingSystem Class: Integrates the blockchain, voter management, and voting functionalities.
load_voters_from_excel(file_path): Loads voter records from an Excel file.
authenticate_voter(): Authenticates a voter by scanning their QR code.
cast_vote(voter_id, candidate): Casts a vote for a specified candidate.
count_votes(): Counts the votes for each candidate.
determine_winner(): Determines the winner based on the vote count.
save_vote_to_excel(voter_id, candidate): Saves vote details to an Excel file.
save_winner_to_excel(winner, votes): Saves the winner details to an Excel file.
scan_qr_code() Function: Captures and decodes QR codes using a webcam.
Usage
Loading Voters: Voter records are loaded from an Excel file named voter.xlsx.
Authentication: Voters authenticate themselves by scanning their QR codes.
Casting Votes: Authenticated voters cast their votes for a specified candidate.
Counting Votes and Determining Winner: The system counts the votes and determines the winner. The results are saved to an Excel file.
Installation
Dependencies(Make sure these modules are made avaialable)
OpenCV
Pyzbar
Pandas
Openpyxl
Running the System
Ensure that the voter.xlsx file is in the same directory as the script and contains the voter records.
Run the script
Follow the prompts to authenticate voters and cast votes.
Conclusion
This project demonstrates a secure and transparent voting system using blockchain technology. By incorporating QR code authentication and Excel integration, it ensures that only registered voters can participate, and their votes are securely recorded and counted. This approach enhances the integrity and trustworthiness of the voting process.
