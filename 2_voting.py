#!/usr/bin/env python3

# Imports
import os
import json  # To work with JSON data
import hashlib  # For generating SHA-1 hash
from phe import paillier  # Import the paillier library for encryption
import base64
from io import BytesIO
import qrcode
import brotli
from PIL import Image


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
        "\nHere is your encrypted vote. Please provide it back to the person running the tally:\n\n",
        vote_json,
        "\n\n",
    )

    # Generate SHA-1 hash to allow voters to verify their vote
    hash_suffix = generate_sha1_hash(vote_json)
    print(
        f"Last 6 characters of SHA-1 hash of your encrypted vote. Remember this and you can verify that your vote goes in.\n\n{hash_suffix}\n\n"
    )

    # Save the vote to a file
    filename = f"vote_{hash_suffix}.json"
    with open(filename, "w") as f:
        f.write(vote_json)

    print(
        """The remainder of the program concerns making a transferable copy of your vote as a QR code.
It generates secure representation of your vote as a QR code which could be printed out and dropped in the ballot box.\n"""
    )
    qr_choice = input("Do you want to see your vote as a QR code? (Y/N)\n").lower()
    if qr_choice in ["yes", "y"]:
        compress_and_generate_qr(vote_dict)


# Function to load public key from stdin
def load_public_key_from_stdin():
    key_data_str = input("Please provide the public key as JSON:\n")
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
        vote = input("\n\nVote for Alice or Bob:\n").lower()
        if vote in ["alice", "bob"]:
            return vote
        print("Invalid choice. Please vote for Alice or Bob.")


# 🛑

# 👇 Everything from here out is fluff. It is concerned with making a QR code / physical copy of the vote.


def integer_to_base64(integer_value):
    integer_value = int(integer_value)
    # Converting integer to bytes
    int_bytes = integer_value.to_bytes(
        (integer_value.bit_length() + 7) // 8, byteorder="big"
    )
    # Encoding bytes to base64
    return base64.b64encode(int_bytes).decode()


def compress_and_resize_png(png_bytes, compression_level=9, resize_factor=0.40):
    # Load the original PNG image from bytes
    original_image = Image.open(BytesIO(png_bytes))

    # Resize the image
    new_size = tuple([int(dim * resize_factor) for dim in original_image.size])
    resized_image = original_image.resize(new_size)

    # Save the compressed and resized image to bytes
    output_buffer = BytesIO()
    resized_image.save(output_buffer, format="PNG", compress_level=compression_level)
    compressed_resized_bytes = output_buffer.getvalue()

    return compressed_resized_bytes


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

    # Estimate QR code width
    qr = qrcode.QRCode(version=1)
    qr.add_data(json.dumps(data))
    qr.make(fit=True)
    estimated_qr_width = (
        len(qr.get_matrix()[0]) * 2
    )  # 2 characters for each cell in the QR code

    # Get current terminal width
    rows, columns = os.popen("stty size", "r").read().split()
    current_terminal_width = int(columns)

    # Ask the user if they want to print the QR code to the terminal
    print_qr_choice = input(
        f"Do you want to print the QR code to the terminal? (Y/N) [Recommended Terminal Width: {estimated_qr_width}, Your Current Terminal Width: {current_terminal_width}]:\n"
    ).lower()
    if print_qr_choice in ["yes", "y"]:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(encoded_data)
        qr.make(fit=True)
        qr_matrix = qr.get_matrix()

        for row in qr_matrix:
            print("".join("##" if cell else "  " for cell in row))

    # Step 2: Base64 encode the compressed data to make it URL-safe
    encoded_data = base64.b64encode(compressed_data).decode()

    # Calculate the length of the encoded data
    encoded_data_length = len(encoded_data)

    # Ask the user if they want to generate a URL-safe QR code
    url_qr_choice = input(
        f"Do you want to generate a QR code URL to put in your browser address bar? (Y/N) [Encoded Data Length: {encoded_data_length} bytes]:\n"
    ).lower()
    if url_qr_choice in ["yes", "y"]:
        qr_image = qrcode.make(encoded_data)

        # prepare io buffer of PNG data
        buffer = BytesIO()
        qr_image.save(buffer)
        buffer.seek(0)

        # Now compress and resize the PNG
        original_png_bytes = buffer.read()
        compressed_resized_bytes = compress_and_resize_png(original_png_bytes)

        # Replace the original PNG bytes with the compressed and resized bytes
        buffer = BytesIO(compressed_resized_bytes)

        # Assume `buffer` contains your QR code in PNG format as bytes.
        buffer.seek(0)
        png_data = buffer.read()
        base64_png = base64.b64encode(png_data).decode()
        data_url = f"data:image/png;base64,{base64_png}"

        print(
            "Copy this into your browser address bar for a QR code of your vote:\n",
            data_url,
        )

        buffer.seek(0)
        with open("output_qr.png", "wb") as f:
            f.write(buffer.read())

        buffer.seek(0)
    return buffer


# Entry point of the program
if __name__ == "__main__":
    main()
