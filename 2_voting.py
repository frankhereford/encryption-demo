#!/usr/bin/env python3

import random
import string

from phe import paillier
import json
import hashlib

def load_public_key_from_stdin():
    key_data_str = input("Please provide the public key as JSON: ")
    key_data = json.loads(key_data_str)
    return paillier.PaillierPublicKey(n=key_data['n'])

def generate_sha1_hash(data):
    sha1 = hashlib.sha1()
    sha1.update(data.strip().encode())
    return sha1.hexdigest()[-6:]

def get_vote():
    while True:
        vote = input("\n\nVote for Alice or Bob: ").lower()
        if vote in ['alice', 'bob']:
            return vote
        else:
            print("Invalid choice. Please vote for Alice or Bob.")

def generate_random_filename():
    random_str = ''.join(random.choices(string.hexdigits, k=6))
    filename = f"vote_{random_str}.json"
    return filename

def main():
    # Step 1: Load the public key
    public_key = load_public_key_from_stdin()

    # Step 2: Get the user's vote
    vote = get_vote()

    # Step 3: Encrypt the votes
    vote_for_alice = 1 if vote == 'alice' else 0
    vote_for_bob = 1 if vote == 'bob' else 0

    encrypted_vote_alice = public_key.encrypt(vote_for_alice)
    encrypted_vote_bob = public_key.encrypt(vote_for_bob)

    # Step 4: Put encrypted votes into dictionary
    vote_dict = {
        'alice': str(encrypted_vote_alice.ciphertext()),
        'bob': str(encrypted_vote_bob.ciphertext())
    }

    # Step 5: Serialize to JSON and print
    vote_json = json.dumps(vote_dict)
    print("Here is your encrypted vote. Please provide it back to the person running the tally:\n\n", vote_json, "\n\n")

    # Generate SHA-1 hash and print last 6 characters
    hash_suffix = generate_sha1_hash(vote_json)
    print(f"Last 6 characters of SHA-1 hash of encrypted vote. Remember this and you can verify that your vote goes in.\n\n{hash_suffix}\n\n")

    filename = f"vote_{hash_suffix}.json"
    with open(filename, 'w') as f:
        f.write(vote_json)

if __name__ == "__main__":
    main()
