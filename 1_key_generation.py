#!/usr/bin/env python3

# Imports
import glob  # To search for files matching a pattern
import os  # To handle OS-level operations like deleting files
from phe import paillier  # Import the paillier library for encryption
import json  # To work with JSON formatted data


# Function to remove all JSON files in the current directory
def remove_json_files():
    # Iterate through each file ending with .json
    for filename in glob.glob("*.json"):
        os.remove(filename)  # Remove the file
    for filename in glob.glob("*.png"):
        os.remove(filename)  # Remove the file


# Remove existing JSON files to start fresh
remove_json_files()

# Step 1: Generate a Public-Private KeyPair for Paillier encryption
public_key, private_key = paillier.generate_paillier_keypair()

# Convert the generated keys to dictionary format for easier handling
public_key_dict = {"g": public_key.g, "n": public_key.n}
private_key_dict = {"p": private_key.p, "q": private_key.q}

# Serialize (convert to JSON format) parts of the private key
# We separate p and q components for multi-party computation
party_a_key_part = json.dumps({"p": private_key_dict["p"]})
party_b_key_part = json.dumps({"q": private_key_dict["q"]})
public_key_json = json.dumps(public_key_dict)

# Export the partial keys as JSON files
# Party A gets 'p', and Party B gets 'q'
with open("party_a_key.json", "w") as f:
    f.write(party_a_key_part)
with open("party_b_key.json", "w") as f:
    f.write(party_b_key_part)

# Export the public key as a JSON file
with open("public_key.json", "w") as f:
    f.write(public_key_json)

# Output instructions for key distribution
print()
print("Give this key to Alice️: ", party_a_key_part, "\n")
print("Give this key to Bob️: ", party_b_key_part, "\n")
print("Publish the public key to voters: ", public_key_json, "\n")
