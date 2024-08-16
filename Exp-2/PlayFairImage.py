from PIL import Image
from pprint import pprint
import numpy as np
from typing import List
import matplotlib.pyplot as plt

def generate_matrix_from_image(key_image_path: str) -> List[List[int]]:
    key_img = Image.open(key_image_path).convert('L')  # Convert to grayscale
    pixels = list(key_img.getdata())
    unique_pixels = []
    seen = set()
    for pixel in pixels:
        if pixel not in seen and len(unique_pixels) < 256:
            seen.add(pixel)
            unique_pixels.append(pixel)
    
    if len(unique_pixels) < 256:
        remaining = [x for x in range(256) if x not in unique_pixels]
        unique_pixels.extend(remaining[:256-len(unique_pixels)])
    
    matrix = [unique_pixels[i*16:(i+1)*16] for i in range(16)]
    return matrix

def encrypt_playfair_image(matrix: List[List[int]], image: Image.Image) -> Image.Image:
    img = image.convert('L')  # Convert to grayscale for encryption
    pixels = list(img.getdata())
    
    lookup = {val: (i, j) for i, row in enumerate(matrix) for j, val in enumerate(row)}
    
    encrypted_pixels = []
    i = 0
    while i < len(pixels):
        pixel1 = pixels[i]
        pixel2 = pixels[i+1] if i+1 < len(pixels) else 0
        
        if pixel1 not in lookup:
            pixel1 = 0
        if pixel2 not in lookup:
            pixel2 = 0
        
        row1, col1 = lookup[pixel1]
        row2, col2 = lookup[pixel2]
        
        if row1 == row2:
            encrypted_pixels.extend([matrix[row1][(col1 + 1) % 16], matrix[row2][(col2 + 1) % 16]])
        elif col1 == col2:
            encrypted_pixels.extend([matrix[(row1 + 1) % 16][col1], matrix[(row2 + 1) % 16][col2]])
        else:
            encrypted_pixels.extend([matrix[row1][col2], matrix[row2][col1]])
        
        i += 2
    
    encrypted_image = Image.new('L', img.size)
    encrypted_image.putdata(encrypted_pixels)
    return encrypted_image

def decrypt_playfair_image(matrix: List[List[int]], encrypted_image: Image.Image) -> Image.Image:
    pixels = list(encrypted_image.getdata())
    
    lookup = {val: (i, j) for i, row in enumerate(matrix) for j, val in enumerate(row)}
    
    decrypted_pixels = []
    i = 0
    while i < len(pixels):
        pixel1 = pixels[i]
        pixel2 = pixels[i+1] if i+1 < len(pixels) else 0
        
        if pixel1 not in lookup:
            pixel1 = 0
        if pixel2 not in lookup:
            pixel2 = 0
        
        row1, col1 = lookup[pixel1]
        row2, col2 = lookup[pixel2]
        
        if row1 == row2:
            decrypted_pixels.extend([matrix[row1][(col1 - 1) % 16], matrix[row2][(col2 - 1) % 16]])
        elif col1 == col2:
            decrypted_pixels.extend([matrix[(row1 - 1) % 16][col1], matrix[(row2 - 1) % 16][col2]])
        else:
            decrypted_pixels.extend([matrix[row1][col2], matrix[row2][col1]])
        
        i += 2
    
    decrypted_image = Image.new('L', encrypted_image.size)
    decrypted_image.putdata(decrypted_pixels)
    return decrypted_image

def display_images(key_image_path, input_image, encrypted_image, decrypted_image):
    plt.figure(figsize=(10, 10))
    
    # Key image (colorful)
    plt.subplot(2, 2, 1)
    plt.imshow(Image.open(key_image_path))
    plt.title('Key Image')
    plt.axis('off')
    
    # Input image (colorful)
    plt.subplot(2, 2, 2)
    plt.imshow(input_image)
    plt.title('Input Image')
    plt.axis('off')
    
    # Encrypted image (grayscale)
    plt.subplot(2, 2, 3)
    plt.imshow(encrypted_image, cmap='gray')
    plt.title('Encrypted Image')
    plt.axis('off')
    
    # Decrypted image (grayscale)
    plt.subplot(2, 2, 4)
    plt.imshow(decrypted_image, cmap='gray')
    plt.title('Decrypted Image')
    plt.axis('off')
    
    plt.show()

if __name__ == "__main__":
    key_image_path = "Tulips.jpg"
    input_image_path = "scenery.jpg"
    encrypted_image_path = "encrypted_image.png"
    decrypted_image_path = "decrypted_image.png"

    matrix = generate_matrix_from_image(key_image_path)
    pprint(matrix)
    
    input_image = Image.open(input_image_path).convert('RGB')
    encrypted_image = encrypt_playfair_image(matrix, input_image)
    encrypted_image.save(encrypted_image_path)
    
    decrypted_image = decrypt_playfair_image(matrix, encrypted_image)
    decrypted_image.save(decrypted_image_path)
    
    display_images(key_image_path, input_image, encrypted_image, decrypted_image)

    print("Encryption and decryption completed. Check the output images.")
