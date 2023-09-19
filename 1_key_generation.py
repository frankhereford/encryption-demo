#!/usr/bin/env python3

import glob
import os
from phe import paillier
import json

def remove_json_files():
    for filename in glob.glob("*.json"):
        os.remove(filename)
        #print(f"Removed {filename}")

remove_json_files()

# Step 1: Generate KeyPair
public_key, private_key = paillier.generate_paillier_keypair()

# Manually convert keys to dictionary
public_key_dict = {
    'g': public_key.g,
    'n': public_key.n
}
private_key_dict = {
    'p': private_key.p,
    'q': private_key.q
}

# "Split" the full private key into two halves
# Here, we just separate out the two main components of the private key: p and q
party_a_key_part = json.dumps({'p': private_key_dict["p"]})
party_b_key_part = json.dumps({'q': private_key_dict["q"]})
public_key_json = json.dumps(public_key_dict)

# Export partial keys for Party A and Party B
with open('party_a_key.json', 'w') as f:
    f.write(party_a_key_part) # such as to a flash drive to be handed to Party A

with open('party_b_key.json', 'w') as f:
    f.write(party_b_key_part) # such as to a flash drive to be handed to Party B

with open('public_key.json', 'w') as f:
    f.write(public_key_json) # such as to be widely published


print()
print("Give this key to Alice️: ", party_a_key_part, "\n")
print("Give this key to Bob️: ", party_b_key_part, "\n")
print("Publish the public key to voters: ", public_key_json, "\n")
