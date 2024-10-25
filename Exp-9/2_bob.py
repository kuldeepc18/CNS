import socket
import random

# Public prime number and base
p = 23  # A large prime number
g = 5   # A primitive root modulo p

# Function to perform modular exponentiation
def mod_exp(base, exp, mod):
    return pow(base, exp, mod)

# Initialize server (Bob)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 12345))
server.listen(1)
print("Server (Bob) started, waiting for connection...")

# Accept connection
conn, addr = server.accept()
print(f"Connected by Eve (actually Bob thinks it's Alice): {addr}")

# Bob's private and public key
bob_private_key = random.randint(1, p - 1)
bob_public_key = mod_exp(g, bob_private_key, p)

# Receive public key from Eve (who's pretending to be Alice)
eve_public_key = int(conn.recv(1024).decode())
print(f"Received Eve's (pretending to be Alice) public key: {eve_public_key}")

# Send Bob's public key to Eve
conn.sendall(str(bob_public_key).encode())

# Compute shared secret with Eve (pretending to be Alice)
shared_secret_bob_eve = mod_exp(eve_public_key, bob_private_key, p)
print(f"Shared secret between Bob and Eve (who's pretending to be Alice): {shared_secret_bob_eve}")

# Close the connection
conn.close()
