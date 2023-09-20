#!/usr/bin/env python3

# Imports
import random  # For generating random numbers
import string  # For string manipulation
import json  # To work with JSON data
import hashlib  # For generating SHA-1 hash
from phe import paillier  # Import the paillier library for encryption


# Function to load public key from stdin (Standard Input)
def load_public_key_from_stdin():
    key_data_str = input("Please provide the public key as JSON: ")
    key_data = json.loads(key_data_str)
    return paillier.PaillierPublicKey(n=key_data["n"])


# Function to generate SHA-1 hash of given data
def generate_sha1_hash(data):
    sha1 = hashlib.sha1()
    sha1.update(data.strip().encode())
    return sha1.hexdigest()[-6:]


# Function to get the user's vote
def get_vote():
    while True:
        vote = input("\n\nVote for Alice or Bob: ").lower()
        if vote in ["alice", "bob"]:
            return vote
        print("Invalid choice. Please vote for Alice or Bob.")


# Main program logic
def main():
    # Load the public key
    public_key = load_public_key_from_stdin()

    # Get the user's vote
    vote = get_vote()

    # Encrypt the vote based on the chosen candidate
    encrypted_vote_alice = public_key.encrypt(1 if vote == "alice" else 0)
    encrypted_vote_bob = public_key.encrypt(1 if vote == "bob" else 0)

    # Store encrypted votes in a dictionary
    vote_dict = {
        "alice": str(encrypted_vote_alice.ciphertext()),
        "bob": str(encrypted_vote_bob.ciphertext()),
    }

    # Serialize the dictionary to JSON
    vote_json = json.dumps(vote_dict)

    # Output the encrypted vote
    print(
        "Here is your encrypted vote. Please provide it back to the person running the tally:\n\n",
        vote_json,
        "\n\n",
    )

    # Generate SHA-1 hash to allow voters to verify their vote
    hash_suffix = generate_sha1_hash(vote_json)
    print(
        f"Last 6 characters of SHA-1 hash of encrypted vote. Remember this and you can verify that your vote goes in.\n\n{hash_suffix}\n\n"
    )

    # Save the vote to a file
    filename = f"vote_{hash_suffix}.json"
    with open(filename, "w") as f:
        f.write(vote_json)


# Entry point of the program
if __name__ == "__main__":
    main()
