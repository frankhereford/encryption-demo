#!/usr/bin/env python3

# Imports
import json  # To work with JSON data
import hashlib  # For generating SHA-1 hash
from phe import paillier  # Import the paillier library for encryption
import base64
from io import BytesIO
import qrcode
import brotli


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


def integer_to_base64(integer_value):
    integer_value = int(integer_value)
    # Converting integer to bytes
    int_bytes = integer_value.to_bytes((integer_value.bit_length() + 7) // 8, byteorder='big')
    # Encoding bytes to base64
    return base64.b64encode(int_bytes).decode()

def compress_and_generate_qr(data):
    # print("input data length", len(json.dumps(data).encode()))

    # Transform large integers to base64
    for key in data.keys():
        original_value = data[key]
        data[key] = integer_to_base64(original_value)
        
        # Print for debugging
        # print(f"{key}: Original value: {original_value}")
        # print(f"{key}: Transformed value: {data[key]}")

    compressed_data = brotli.compress(json.dumps(data).encode())
    
    # Step 2: Base64 encode the compressed data to make it URL-safe
    encoded_data = base64.b64encode(compressed_data).decode()
    
    # print("Compressed Data length: ", len(encoded_data))
    
    # Step 3: Generate a QR code from the base64 encoded data

    # Ask the user if they want to print the QR code to the terminal
    print_qr_choice = input("Do you want to print the QR code to the terminal? (Yes/Y): ").lower()
    if print_qr_choice in ['yes', 'y']:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(encoded_data)
        qr.make(fit=True)
        qr_matrix = qr.get_matrix()

        for row in qr_matrix:
            print("".join("##" if cell else "  " for cell in row))
    
    # Ask the user if they want to generate a URL-safe QR code
    url_qr_choice = input("Do you want to generate a QR code URL to put in your browser address bar? (Yes/Y): ").lower()
    if url_qr_choice in ['yes', 'y']:
        qr_image = qrcode.make(encoded_data)
        
        # prepare io buffer of PNG data
        buffer = BytesIO()
        qr_image.save(buffer)
        buffer.seek(0)
        
        # Assume `buffer` contains your QR code in PNG format as bytes.
        buffer.seek(0)
        png_data = buffer.read()
        base64_png = base64.b64encode(png_data).decode()
        data_url = f"data:image/png;base64,{base64_png}"

        print("Copy this into your browser address bar for a QR code of your vote:", data_url)
        
        buffer.seek(0)
        with open("output_qr.png", "wb") as f:
            f.write(buffer.read())
        
        buffer.seek(0)
    return buffer

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

    compress_and_generate_qr(vote_dict)
    



# Entry point of the program
if __name__ == "__main__":
    main()
