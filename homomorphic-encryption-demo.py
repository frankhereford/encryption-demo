#!/usr/bin/env python3

from phe import paillier
import hashlib
import json

def generate_keys():
    # Generate public and private keys
    global public_key
    global private_key
    public_key, private_key = paillier.generate_paillier_keypair()

    #print("public key object: ", public_key)
    #print("private key object: ", private_key)

    print()

    public_key_dict = {
    'n': get_last_6_sha1(public_key.n),
    'g': get_last_6_sha1(public_key.g)
    }

    print("Public Key Contents: ", json.dumps(public_key_dict))

    private_key_dict = {
        'p': get_last_6_sha1(private_key.p),
        'q': get_last_6_sha1(private_key.q)
    }

    print("Private Key Contents: ", json.dumps(private_key_dict))

    print()

def fully_homomorphic_encryption_addition():

    # Encrypt three numbers
    encrypted_three = public_key.encrypt(3)
    encrypted_seven = public_key.encrypt(7)
    encrypted_zero = public_key.encrypt(0)

    print("Encrypted_three: ", get_last_6_sha1(encrypted_three.ciphertext()), "\n")
    print("Encrypted_seven: ", get_last_6_sha1(encrypted_seven.ciphertext()), "\n")
    print("Encrypted_zero: ", get_last_6_sha1(encrypted_zero.ciphertext()), "\n")

    # Add the encrypted numbers
    encrypted_sum_of_three_and_seven = encrypted_three + encrypted_seven
    encrypted_three_add_zero = encrypted_three + encrypted_zero

    print(f"Encrypted sum of encrypted 3 and encrypted 7: {get_last_6_sha1(encrypted_sum_of_three_and_seven.ciphertext())}", "\n")
    print(f"Encrypted three with encrypted zero added to it: {get_last_6_sha1(encrypted_three_add_zero.ciphertext())}", "\n")

    # Decrypt the sums
    decrypted_sum_3_and_7 = private_key.decrypt(encrypted_sum_of_three_and_seven)
    decrypted_sum_3_and_0 = private_key.decrypt(encrypted_three_add_zero)

    print(f"Decrypted sum of encrypted 3 and encrypted 7: {decrypted_sum_3_and_7}", "\n")
    print(f"Decrypted sum of encrypted 3 and encrypted 0: {decrypted_sum_3_and_0}", "\n")

def partial_homomorphic_encryption_multiplication():
    encrypted_three = public_key.encrypt(3)
    plaintext_number1 = 11 

    print("encrypted_three: ", get_last_6_sha1(encrypted_three.ciphertext()), "\n")

    # Add the encrypted numbers
    encrypted_product = encrypted_three * plaintext_number1

    print(f"Encrypted product of encrypted 3 and plaintext 11: {get_last_6_sha1(encrypted_product.ciphertext())}", "\n")

    # Decrypt the product
    decrypted_product = private_key.decrypt(encrypted_product)

    print(f"Decrypted product: {decrypted_product}")

def get_last_6_sha1(input_str):
    sha1 = hashlib.sha1()
    sha1.update(str(input_str).encode())
    full_hash = sha1.hexdigest()
    return str(input_str)[:10] + '...' + str(input_str)[-10:] + ' (' + full_hash[-6:] + ')'


if __name__ == "__main__":
    print("🔐  Generating a public/private key pair")
    generate_keys()

    print("🪄  Fully Homomorphic Encryption Addition\n")
    fully_homomorphic_encryption_addition()

    print("✨  Partial Homomorphic Encryption Multiplication\n")
    partial_homomorphic_encryption_multiplication()
