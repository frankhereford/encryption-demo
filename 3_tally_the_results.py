#!/usr/bin/env python3

# Imports
from phe import paillier  # For Paillier encryption
import json  # To work with JSON data
import hashlib  # For generating SHA-1 hash

# Function to generate SHA-1 hash of given data
def generate_sha1_hash(data):
    sha1 = hashlib.sha1()
    sha1.update(data.strip().encode())
    return sha1.hexdigest()[-6:]

# Main program logic
def main():
    # Initialize encrypted tallies for Alice and Bob to zero
    public_key_data = json.loads(input("Please provide the public key as JSON: "))
    public_key = paillier.PaillierPublicKey(n=public_key_data['n'])
    
    encrypted_tally_alice = public_key.encrypt(0)
    encrypted_tally_bob = public_key.encrypt(0)

    # Loop to collect encrypted votes
    while True:
        encrypted_vote_str = input("Please provide encrypted vote as JSON (or press Enter to finish): ")
        
        # Break the loop if input is empty
        if encrypted_vote_str == "":
            break

        # Generate SHA-1 hash of encrypted vote for verification
        hash_suffix = generate_sha1_hash(encrypted_vote_str)
        print(f"\nLast 6 characters of SHA-1 hash:\n{hash_suffix}\n")

        # Deserialize the encrypted vote from JSON
        encrypted_vote_data = json.loads(encrypted_vote_str)

        # Convert JSON data to Paillier Encrypted Numbers
        encrypted_vote_alice = paillier.EncryptedNumber(public_key, int(encrypted_vote_data['alice']))
        encrypted_vote_bob = paillier.EncryptedNumber(public_key, int(encrypted_vote_data['bob']))
        
        # Add the new votes to the tally
        encrypted_tally_alice += encrypted_vote_alice
        encrypted_tally_bob += encrypted_vote_bob

    # Serialize the final tallies to JSON
    tally_dict = {
        'alice': str(encrypted_tally_alice.ciphertext()),
        'bob': str(encrypted_tally_bob.ciphertext())
    }
    tally_json = json.dumps(tally_dict)
    print("Final encrypted tally:", tally_json)

    # Save the final encrypted tally to a JSON file
    with open("encrypted_tally.json", 'w') as f:
        f.write(tally_json)

# Entry point of the program
if __name__ == "__main__":
    main()
