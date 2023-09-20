#!/usr/bin/env python3

# Imports
from phe import paillier  # For Paillier encryption
import json  # To work with JSON data


# Function to load partial key data from the user input
def load_partial_key_from_stdin(label):
    partial_key_data_str = input(
        f"Please provide the partial key for {label} as JSON: "
    )
    return json.loads(partial_key_data_str)


# Main program logic
def main():
    # Load the encrypted tally for the election
    tally_data_str = input(
        "Please provide the encrypted tallies for Alice and Bob as JSON: "
    )
    tally_data = json.loads(tally_data_str)

    # Load the public key data from the user input
    public_key_data = json.loads(input("Please provide the public key as JSON: "))
    public_key = paillier.PaillierPublicKey(n=public_key_data["n"])

    # Convert JSON data to Paillier Encrypted Numbers for tallies
    encrypted_tally_alice = paillier.EncryptedNumber(
        public_key, int(tally_data["alice"])
    )
    encrypted_tally_bob = paillier.EncryptedNumber(public_key, int(tally_data["bob"]))

    # Reconstruct the full private key using partial keys
    partial_key_a = load_partial_key_from_stdin("Alice")
    partial_key_b = load_partial_key_from_stdin("Bob")

    full_private_key = paillier.PaillierPrivateKey(
        public_key=public_key, p=int(partial_key_a["p"]), q=int(partial_key_b["q"])
    )

    # Decrypt the final tallies and display them
    final_tally_alice = full_private_key.decrypt(encrypted_tally_alice)
    final_tally_bob = full_private_key.decrypt(encrypted_tally_bob)

    print(
        f"\n\nFinal tally:\n\nAlice = {final_tally_alice}\n\nBob = {final_tally_bob}\n\n"
    )


# Entry point for the program
if __name__ == "__main__":
    main()
