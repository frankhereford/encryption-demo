#!/usr/bin/env python3

from phe import paillier
import json
import hashlib

def generate_sha1_hash(data):
    sha1 = hashlib.sha1()
    sha1.update(data.strip().encode())
    return sha1.hexdigest()[-6:]

def main():
    # Initialize encrypted tallies for Alice and Bob to zero
    public_key_data = json.loads(input("Please provide the public key as JSON: "))
    public_key = paillier.PaillierPublicKey(n=public_key_data['n'])
    
    encrypted_tally_alice = public_key.encrypt(0)
    encrypted_tally_bob = public_key.encrypt(0)

    # Collect encrypted votes
    while True:
        encrypted_vote_str = input("Please provide encrypted vote as JSON (or press Enter to finish): ")
        if encrypted_vote_str == "":
            break

        # Generate and print SHA-1 hash
        hash_suffix = generate_sha1_hash(encrypted_vote_str)
        print(f"Last 6 characters of SHA-1 hash: {hash_suffix}")


        encrypted_vote_data = json.loads(encrypted_vote_str)
        
        encrypted_vote_alice = paillier.EncryptedNumber(public_key, int(encrypted_vote_data['alice']))
        encrypted_vote_bob = paillier.EncryptedNumber(public_key, int(encrypted_vote_data['bob']))
        
        encrypted_tally_alice += encrypted_vote_alice
        encrypted_tally_bob += encrypted_vote_bob

    # Serialize tallies to JSON
    tally_dict = {
        'alice': str(encrypted_tally_alice.ciphertext()),
        'bob': str(encrypted_tally_bob.ciphertext())
    }
    tally_json = json.dumps(tally_dict)
    print("Final encrypted tally:", tally_json)

    with open("encrypted_tally.json", 'w') as f:
        f.write(tally_json)

if __name__ == "__main__":
    main()
