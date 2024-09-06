import time
from Crypto.Cipher import DES
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
DESInitVector = get_random_bytes(DES.block_size)
print(f'Initialization Vector (binary) = {to_binary_string(DESInitVector)}')

# Define DES key
des_key = b'EightBit'
print(f'Key (binary) = {to_binary_string(des_key)}')

# Encrypt plaintext
des_cipher = DES.new(des_key, DES.MODE_CBC, DESInitVector)
des_ciphertext = des_cipher.encrypt(pad(plaintext, DES.block_size))
print(f'Ciphertext (binary) = {to_binary_string(des_ciphertext)}')

# Measure encryption time
etime = time.time()
print(f'Encryption Time = {etime - stime:.20f} seconds')

# Decrypt ciphertext
cipher_des_decrypt = DES.new(des_key, DES.MODE_CBC, DESInitVector)
plaintext_decrypted_des = unpad(cipher_des_decrypt.decrypt(des_ciphertext), DES.block_size)
print(f'Decrypted Plaintext (binary): {to_binary_string(plaintext_decrypted_des)}')

# Measure decryption time
print(f'Decryption Time = {time.time() - etime:.20f} seconds')
print()

# Avalanche effect 1 - Change in plaintext
print('Avalanche effect 1 - Change in plaintext')
plaintext = b'Hello@123'
print(f'Plain text (binary) = {to_binary_string(plaintext)}')

# Generate new initialization vector
DESInitVector = get_random_bytes(DES.block_size)
print(f'Initialization Vector (binary) = {to_binary_string(DESInitVector)}')

# Encrypt new plaintext
des_cipher = DES.new(des_key, DES.MODE_CBC, DESInitVector)
des_ciphertext = des_cipher.encrypt(pad(plaintext, DES.block_size))
print(f'Ciphertext (binary) = {to_binary_string(des_ciphertext)}')

# Decrypt new ciphertext
cipher_des_decrypt = DES.new(des_key, DES.MODE_CBC, DESInitVector)
plaintext_decrypted_des = unpad(cipher_des_decrypt.decrypt(des_ciphertext), DES.block_size)
print(f'Decrypted Plaintext (binary): {to_binary_string(plaintext_decrypted_des)}')
print()

# Avalanche effect 2 - Change in key
print('Avalanche effect 2 - Change in key')
plaintext = b'Hello@123'
print(f'Plain text (binary) = {to_binary_string(plaintext)}')

# Generate new initialization vector
DESInitVector = get_random_bytes(DES.block_size)
print(f'Initialization Vector (binary) = {to_binary_string(DESInitVector)}')

# Define new DES key
des_key = b'EightBin'
print(f'Key (binary) = {to_binary_string(des_key)}')

# Encrypt with new key
des_cipher = DES.new(des_key, DES.MODE_CBC, DESInitVector)
des_ciphertext = des_cipher.encrypt(pad(plaintext, DES.block_size))
print(f'Ciphertext (binary) = {to_binary_string(des_ciphertext)}')

# Decrypt with new key
cipher_des_decrypt = DES.new(des_key, DES.MODE_CBC, DESInitVector)
plaintext_decrypted_des = unpad(cipher_des_decrypt.decrypt(des_ciphertext), DES.block_size)
print(f'Decrypted Plaintext (binary): {to_binary_string(plaintext_decrypted_des)}')
