import socket
import random

# Prime number and base (public parameters)
p = 23  # A large prime number
g = 5   # A primitive root modulo p

# Function to perform modular exponentiation
def mod_exp(base, exp, mod):
    return pow(base, exp, mod)

# Create a TCP/IP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 12345))
server.listen(1)
print("Server started, waiting for connection...")

# Accept client connection
conn, addr = server.accept()
print(f"Connected by {addr}")

# Server (Bob) generates private and public keys
private_key = random.randint(1, p - 1)
public_key = mod_exp(g, private_key, p)

# Send server's (Bob's) public key to client
conn.sendall(str(public_key).encode())

# Receive client's (Alice's) public key
client_public_key = int(conn.recv(1024).decode())

# Calculate shared secret key
shared_secret = mod_exp(client_public_key, private_key, p)
print(f"Shared secret key: {shared_secret}")

# Close the connection
conn.close()
