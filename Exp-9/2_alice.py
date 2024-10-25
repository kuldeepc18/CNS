import socket
import random

# Public prime number and base
p = 23  # A large prime number
g = 5   # A primitive root modulo p

# Function to perform modular exponentiation
def mod_exp(base, exp, mod):
    return pow(base, exp, mod)

# Initialize Alice as a client
alice = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
alice.connect(('localhost', 54321))  # Connect to Eve (who's pretending to be Bob)

# Alice's private and public key
alice_private_key = random.randint(1, p - 1)
alice_public_key = mod_exp(g, alice_private_key, p)

# Send Alice's public key to Eve (thinking Eve is Bob)
alice.sendall(str(alice_public_key).encode())

# Receive Eve's public key (pretending to be Bob's public key)
eve_public_key = int(alice.recv(1024).decode())

# Compute shared secret with Eve (thinking it's with Bob)
shared_secret_alice_eve = mod_exp(eve_public_key, alice_private_key, p)
print(f"Shared secret between Alice and Eve (thinking it's Bob): {shared_secret_alice_eve}")

# Close the connection
alice.close()
