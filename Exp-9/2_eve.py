import socket
import random

# Public prime number and base
p = 23  # A large prime number
g = 5   # A primitive root modulo p

# Function to perform modular exponentiation
def mod_exp(base, exp, mod):
    return pow(base, exp, mod)

# Eve connects to Bob pretending to be Alice
eve_to_bob = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
eve_to_bob.connect(('localhost', 12345))

# Eve generates private and public keys (for Alice-Eve connection)
eve_private_key = random.randint(1, p - 1)
eve_public_key = mod_exp(g, eve_private_key, p)

# Eve acts as a server for Alice
eve_as_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
eve_as_server.bind(('localhost', 54321))
eve_as_server.listen(1)
print("Eve (server) started, waiting for Alice...")

# Accept connection from Alice
conn_alice, addr_alice = eve_as_server.accept()
print(f"Connected by Alice: {addr_alice}")

# Step 3: Alice sends her public key to Eve
alice_public_key = int(conn_alice.recv(1024).decode())
print(f"Received Alice's public key: {alice_public_key}")

# Step 4: Eve sends her own public key back to Alice (pretending to be Bob)
conn_alice.sendall(str(eve_public_key).encode())

# Step 5: Eve computes shared secret with Alice (Alice -> Eve)
shared_secret_eve_alice = mod_exp(alice_public_key, eve_private_key, p)
print(f"Shared secret between Alice and Eve: {shared_secret_eve_alice}")

# Step 6: Now Eve performs Diffie-Hellman with Bob
# Send Eve's public key to Bob (pretending it's from Alice)
eve_to_bob.sendall(str(eve_public_key).encode())

# Receive Bob's public key
bob_public_key = int(eve_to_bob.recv(1024).decode())
print(f"Received Bob's public key: {bob_public_key}")

# Compute shared secret between Eve and Bob (Eve -> Bob)
shared_secret_eve_bob = mod_exp(bob_public_key, eve_private_key, p)
print(f"Shared secret between Eve and Bob: {shared_secret_eve_bob}")

# Close connections
conn_alice.close()
eve_to_bob.close()
eve_as_server.close()
