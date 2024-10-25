import socket
import random

# Prime number and base (public parameters)
p = 23  # A large prime number
g = 5   # A primitive root modulo p

# Function to perform modular exponentiation
def mod_exp(base, exp, mod):
    return pow(base, exp, mod)

# Initialize client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 12345))

# Client (Alice) generates private and public keys
private_key = random.randint(1, p - 1)
public_key = mod_exp(g, private_key, p)

# Receive server's (Bob's) public key
server_public_key = int(client.recv(1024).decode())

# Send client's (Alice's) public key to server
client.sendall(str(public_key).encode())

# Calculate shared secret key
shared_secret = mod_exp(server_public_key, private_key, p)
print(f"Shared secret key: {shared_secret}")

# Close the connection
client.close()
