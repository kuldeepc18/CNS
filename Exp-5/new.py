from Crypto.Cipher import AES, DES
from Crypto.Util.Padding import pad, unpad
import binascii
import time

# AES encryption/decryption
def aes_encrypt_decrypt(plaintext, key):
    # Ensure the key is 16 bytes long for AES-128
    key = key.ljust(16, ' ')[:16].encode('utf-8')
    cipher = AES.new(key, AES.MODE_ECB)
    
    # Pad plaintext to be a multiple of block size (16 bytes for AES)
    padded_text = pad(plaintext.encode('utf-8'), 16)
    
    # Encrypt and measure encryption time
    start_time = time.time()
    ciphertext = cipher.encrypt(padded_text)
    encryption_time = time.time() - start_time
    print("AES Ciphertext:", binascii.hexlify(ciphertext).decode('utf-8'))
    print("AES Encryption Time: {:.6f} seconds".format(encryption_time))
    
    # Decrypt and measure decryption time
    start_time = time.time()
    decrypted_text = unpad(cipher.decrypt(ciphertext), 16)
    decryption_time = time.time() - start_time
    print("AES Decrypted Text:", decrypted_text.decode('utf-8'))
    print("AES Decryption Time: {:.6f} seconds".format(decryption_time))

# DES encryption/decryption
def des_encrypt_decrypt(plaintext, key):
    # Ensure the key is 8 bytes long for DES
    key = key.ljust(8, ' ')[:8].encode('utf-8')
    cipher = DES.new(key, DES.MODE_ECB)
    
    # Pad plaintext to be a multiple of block size (8 bytes for DES)
    padded_text = pad(plaintext.encode('utf-8'), 8)
    
    # Encrypt and measure encryption time
    start_time = time.time()
    ciphertext = cipher.encrypt(padded_text)
    encryption_time = time.time() - start_time
    print("DES Ciphertext:", binascii.hexlify(ciphertext).decode('utf-8'))
    print("DES Encryption Time: {:.6f} seconds".format(encryption_time))
    
    # Decrypt and measure decryption time
    start_time = time.time()
    decrypted_text = unpad(cipher.decrypt(ciphertext), 8)
    decryption_time = time.time() - start_time
    print("DES Decrypted Text:", decrypted_text.decode('utf-8'))
    print("DES Decryption Time: {:.6f} seconds".format(decryption_time))

# Test with plaintext and keys
plaintext = "123454"
aes_key = "122"
des_key = "122"

print("AES Encryption/Decryption:")
aes_encrypt_decrypt(plaintext, aes_key)

print("\nDES Encryption/Decryption:")
des_encrypt_decrypt(plaintext, des_key)

