import time
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

def to_binary_string(data):
    """Convert bytes to a binary string."""
    return ' '.join(f'{byte:08b}' for byte in data)

# Measure encryption time
stime = time.time()

# Define plaintext
plaintext = b'Hello@123'
print(f'Plain text (binary) = {to_binary_string(plaintext)}')

# Generate initialization vector
initVector = get_random_bytes(AES.block_size)
print(f'Initialization Vector (binary) = {to_binary_string(initVector)}')

# Define AES key
aes_key = b'MySecretPassword'
print(f'Key (binary) = {to_binary_string(aes_key)}')

# Encrypt plaintext
aes_cipher = AES.new(aes_key, AES.MODE_CBC, initVector)
ciphertext = aes_cipher.encrypt(pad(plaintext, AES.block_size))
print(f'Ciphertext (binary) = {to_binary_string(ciphertext)}')

# Measure encryption time
etime = time.time()
print(f'Encryption Time = {etime - stime:.20f} seconds')

# Decrypt ciphertext
cipher_aes_decrypt = AES.new(aes_key, AES.MODE_CBC, initVector)
plaintext_decrypted = unpad(cipher_aes_decrypt.decrypt(ciphertext), AES.block_size)
print(f'Decrypted Text (binary) = {to_binary_string(plaintext_decrypted)}')

# Measure decryption time
print(f'Decryption Time = {time.time() - etime:.20f} seconds')
print()

# Avalanche effect 1 - Change in plaintext
print("Avalanche effect 1 - Change in plaintext")
plaintext = b'Hello@123'
print(f'Plain text (binary) = {to_binary_string(plaintext)}')

# Generate new initialization vector
initVector = get_random_bytes(AES.block_size)
print(f'Initialization Vector (binary) = {to_binary_string(initVector)}')

# Encrypt new plaintext
aes_cipher = AES.new(aes_key, AES.MODE_CBC, initVector)
ciphertext = aes_cipher.encrypt(pad(plaintext, AES.block_size))
print(f'Ciphertext (binary) = {to_binary_string(ciphertext)}')

# Decrypt new ciphertext
cipher_aes_decrypt = AES.new(aes_key, AES.MODE_CBC, initVector)
plaintext_decrypted = unpad(cipher_aes_decrypt.decrypt(ciphertext), AES.block_size)
print(f'Decrypted Text (binary) = {to_binary_string(plaintext_decrypted)}')
print()

# Avalanche effect 2 - Change in key
print("Avalanche effect 2 - Change in key")
plaintext = b'Hello@123'
print(f'Plain text (binary) = {to_binary_string(plaintext)}')

# Generate new initialization vector
initVector = get_random_bytes(AES.block_size)
print(f'Initialization Vector (binary) = {to_binary_string(initVector)}')

# Define new AES key
aes_key = b'MySecretPasswotd'
print(f'Key (binary) = {to_binary_string(aes_key)}')

# Encrypt with new key
aes_cipher = AES.new(aes_key, AES.MODE_CBC, initVector)
ciphertext = aes_cipher.encrypt(pad(plaintext, AES.block_size))
print(f'Ciphertext (binary) = {to_binary_string(ciphertext)}')

# Decrypt with new key
cipher_aes_decrypt = AES.new(aes_key, AES.MODE_CBC, initVector)
plaintext_decrypted = unpad(cipher_aes_decrypt.decrypt(ciphertext), AES.block_size)
print(f'Decrypted Text (binary) = {to_binary_string(plaintext_decrypted)}')
