import numpy as np
from PIL import Image

# Function to check if a matrix is invertible in mod 256
def is_invertible(matrix, mod=256):
    det = int(round(np.linalg.det(matrix))) % mod
    return det != 0 and np.gcd(det, mod) == 1

# Function to find modular inverse of a matrix in mod 256
def mod_matrix_inverse(matrix, mod=256):
    det = int(round(np.linalg.det(matrix))) % mod
    det_inv = pow(det, -1, mod)  # Inverse of determinant mod 256
    matrix_mod_inv = (
        np.round(det_inv * np.linalg.inv(matrix) * np.linalg.det(matrix))
        .astype(int) % mod
    )
    return matrix_mod_inv

# Function to generate a random 5x5 invertible matrix in mod 256
def generate_random_invertible_matrix(size=5, mod=256):
    while True:
        matrix = np.random.randint(0, mod, (size, size))
        if is_invertible(matrix, mod):
            return matrix

# Encrypt function using Hill cipher
def hill_cipher_encrypt(image, key_matrix):
    # Convert image to numpy array and get its shape
    pixel_values = np.array(image)
    original_shape = pixel_values.shape
    pixel_values = pixel_values.flatten()

    # Padding to make the length a multiple of 5
    padding_length = (5 - len(pixel_values) % 5) % 5
    pixel_values = np.pad(pixel_values, (0, padding_length), mode='constant')

    # Split into groups of 5 pixels
    pixel_groups = np.split(pixel_values, len(pixel_values) // 5)

    # Encrypt each group
    encrypted_pixels = []
    for group in pixel_groups:
        encrypted_group = np.dot(key_matrix, group) % 256
        encrypted_pixels.extend(encrypted_group)

    # Reshape back to original image shape
    encrypted_image = np.array(encrypted_pixels[: len(pixel_values)]).reshape(original_shape)
    return Image.fromarray(encrypted_image.astype(np.uint8))

# Decrypt function using Hill cipher
def hill_cipher_decrypt(encrypted_image, key_matrix):
    # Get inverse of key matrix in mod 256
    key_matrix_inv = mod_matrix_inverse(key_matrix)

    # Convert image to numpy array
    pixel_values = np.array(encrypted_image)
    original_shape = pixel_values.shape
    pixel_values = pixel_values.flatten()

    # Split into groups of 5 pixels
    pixel_groups = np.split(pixel_values, len(pixel_values) // 5)

    # Decrypt each group
    decrypted_pixels = []
    for group in pixel_groups:
        decrypted_group = np.dot(key_matrix_inv, group) % 256
        decrypted_pixels.extend(decrypted_group)

    # Reshape back to original image shape
    decrypted_image = np.array(decrypted_pixels[: len(pixel_values)]).reshape(original_shape)
    return Image.fromarray(decrypted_image.astype(np.uint8))

# Example usage:
if __name__ == "__main__":
    # Open the grayscale image
    image = Image.open("Nature.jpg").convert("L")  # Convert to grayscale

    # Generate a random invertible 5x5 key matrix
    key_matrix = generate_random_invertible_matrix()

    print("Random Invertible Key Matrix:\n", key_matrix)

    # Encrypt the image
    encrypted_image = hill_cipher_encrypt(image, key_matrix)
    encrypted_image.save("hill_encrypted_image.png")

    # Decrypt the image
    decrypted_image = hill_cipher_decrypt(encrypted_image, key_matrix)
    decrypted_image.save("hill_decrypted_image.png")
