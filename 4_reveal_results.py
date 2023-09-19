#!/usr/bin/env python3

from phe import paillier
import json

def load_partial_key_from_stdin(label):
    partial_key_data_str = input(f"Please provide the partial key for {label} as JSON: ")
    return json.loads(partial_key_data_str)

def main():
    # Load encrypted tallies for Alice and Bob
    tally_data_str = input("Please provide the encrypted tallies for Alice and Bob as JSON: ")
    tally_data = json.loads(tally_data_str)

    # Load the public key
    public_key_data = json.loads(input("Please provide the public key as JSON: "))
    public_key = paillier.PaillierPublicKey(n=public_key_data['n'])

    encrypted_tally_alice = paillier.EncryptedNumber(public_key, int(tally_data['alice']))
    encrypted_tally_bob = paillier.EncryptedNumber(public_key, int(tally_data['bob']))

    # Reconstruct the private key
    partial_key_a = load_partial_key_from_stdin('Alice')
    partial_key_b = load_partial_key_from_stdin('Bob')
    
    full_private_key = paillier.PaillierPrivateKey(
        public_key=public_key, 
        p=int(partial_key_a['p']), 
        q=int(partial_key_b['q'])
    )

    # Decrypt and print the final tally
    final_tally_alice = full_private_key.decrypt(encrypted_tally_alice)
    final_tally_bob = full_private_key.decrypt(encrypted_tally_bob)
    
    print(f"Final tally: Alice = {final_tally_alice}, Bob = {final_tally_bob}")

if __name__ == "__main__":
    main()
