import numpy as np
import math
from string import ascii_uppercase, digits, punctuation

def mod_inverse(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def is_invertible(matrix):
    det = int(round(np.linalg.det(matrix))) % 256
    return det != 0 and math.gcd(det, 256) == 1

def generate_random_invertible_matrix(size=2):
    while True:
        matrix = np.random.randint(0, 256, (size, size))
        if is_invertible(matrix):
            return matrix

def preprocess_text(text):
    return ''.join(filter(lambda x: ord(x) < 256, text))

def encrypt(plaintext, key_matrix):
    plaintext = preprocess_text(plaintext)
    n = key_matrix.shape[0]
    padded_length = (len(plaintext) + (n - 1)) // n * n
    plaintext = plaintext.ljust(padded_length, 'X')

    ciphertext = ""
    for i in range(0, len(plaintext), n):
        block = np.array([ord(char) for char in plaintext[i:i+n]])
        encrypted_block = np.dot(key_matrix, block) % 256
        ciphertext += ''.join(chr(num) for num in encrypted_block)
    return ciphertext

def decrypt(ciphertext, key_matrix):
    n = key_matrix.shape[0]
    det = int(round(np.linalg.det(key_matrix))) % 256
    det_inv = mod_inverse(det, 256)

    if det_inv is None:
        raise ValueError("The key matrix is not invertible.")
    key_matrix_inv = np.round(np.linalg.inv(key_matrix) * np.linalg.det(key_matrix)).astype(int) % 256
    key_matrix_inv = (det_inv * key_matrix_inv) % 256

    decrypted_text = ""
    for i in range(0, len(ciphertext), n):
        block = np.array([ord(char) for char in ciphertext[i:i+n]])
        decrypted_block = np.dot(key_matrix_inv, block) % 256
        decrypted_text += ''.join(chr(num) for num in decrypted_block)
    return decrypted_text.rstrip('X')

if __name__ == "__main__":
    key_matrix = generate_random_invertible_matrix(size=2)
    print("Invertible Key Matrix :\n", key_matrix)
    plaintext = input("Enter Text Message : ")
    print("Plaintext :", plaintext)
    encrypted_message = encrypt(plaintext, key_matrix)
    print("Encrypted Text:", encrypted_message)
    decrypted_message = decrypt(encrypted_message, key_matrix)
    print("Decrypted Text:", decrypted_message)