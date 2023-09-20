# encryption-demo: Dual Custody Asymmetric Homomorphic Encryption

## Table of Contents
- [encryption-demo: Dual Custody Asymmetric Homomorphic Encryption](#encryption-demo-dual-custody-asymmetric-homomorphic-encryption)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
    - [Giving the demo](#giving-the-demo)
  - [How It Works](#how-it-works)
    - [Key Generation](#key-generation)
    - [Voting](#voting)
    - [Tallying](#tallying)
    - [Revealing Results](#revealing-results)
  - [Getting Started](#getting-started)
  - [Requirements and Parameters](#requirements-and-parameters)
  - [Tech Stack](#tech-stack)
  - [FAQ](#faq)

## Overview
This demo provides a simplified example of a secure voting system that incorporates dual-custody asymmetric homomorphic encryption. It aims to demonstrate that a fair and verifiable election can be conducted even when the involved parties do not fully trust each other.

### Giving the demo

To give the demo:
```
docker compose run demo
```

To vote, run:
```
docker run -it frankinaustin/dev-sync-demo:latest
```


## How It Works

### Key Generation
- Script: 1_key_generation.py
- Generates a pair of public and private keys using Paillier encryption.
- The private key is divided into two parts: one for Alice and one for Bob.
### Voting
- Script: 2_voting.py
- Voters can cast their votes for either Alice or Bob.
- Each vote is encrypted using the public key generated during key generation.
- Encrypted votes are saved as .json files and hashed for verification.

### Tallying
- Script: 3_tally_the_results.py
- Aggregates the encrypted votes.
- The poll conductor can tally the votes without revealing the actual vote counts.

### Revealing Results
- Script: 4_reveal_results.py
- Both Alice's and Bob's partial keys are needed to decrypt the final tally.
- The final tally is revealed only when both parties agree to decrypt it.

## Getting Started
To initiate the demo, run:
To cast a vote, execute:

## Requirements and Parameters
- Alice and Bob may not trust each other but can cooperate for a fair election.
- Voters should be able to verify that their vote is counted and remains private.
- The poll conductor can aggregate the encrypted votes but cannot see the actual results.
- Decryption and result revelation require the consent of both Alice and Bob.

## Tech Stack
- Python 3.x
- Docker
- Paillier Cryptosystem
- SHA-1 Hashing

## FAQ
Q: Can the person conducting the poll see individual votes?  
A: No, they can only see the encrypted votes.

Q: What happens if one of the parties refuses to reveal their part of the private key?  
A: The results cannot be decrypted and will therefore not be revealed.
