import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def get_user_matrix():
    print("Enter the 16x16 matrix elements row by row.")
    print("Separate elements with spaces, and press Enter after each row.")
    matrix = []
    for i in range(16):
        while True:
            try:
                row = list(map(int, input(f"Enter row {i+1}: ").split()))
                if len(row) != 16:
                    raise ValueError("Each row must contain exactly 16 elements.")
                matrix.append(row)
                break
            except ValueError as e:
                print(f"Invalid input: {e}. Please try again.")
    return np.array(matrix)

def is_invertible(matrix):
    return np.linalg.det(matrix) != 0

def encrypt_decrypt_image(image_path, key_matrix):
    try:
        # Read the image
        img = Image.open(image_path)
        img_array = np.array(img)
        
        # Convert to RGB if image is RGBA
        if img_array.ndim == 3 and img_array.shape[2] == 4:
            img = img.convert('RGB')
            img_array = np.array(img)
        
        # Ensure the image is 3D (RGB)
        if img_array.ndim == 2:
            img_array = np.stack((img_array,)*3, axis=-1)
        
        height, width, channels = img_array.shape

        # Convert to grayscale for encryption
        img_gray = img.convert('L')
        img_gray_array = np.array(img_gray)

        # Pad the image if necessary
        pad_height = (16 - height % 16) % 16
        pad_width = (16 - width % 16) % 16
        img_padded = np.pad(img_gray_array, ((0, pad_height), (0, pad_width)), mode='constant')

        # Reshape the image into 16x16 blocks
        blocks = img_padded.reshape((-1, 16, 16))

        # Encrypt
        encrypted_blocks = np.array([np.dot(key_matrix, block) % 256 for block in blocks]).astype(int)
        encrypted_img = encrypted_blocks.reshape(img_padded.shape)

        # Decrypt
        inv_key_matrix = np.linalg.inv(key_matrix)
        decrypted_blocks = np.array([np.round(np.dot(inv_key_matrix, block)) % 256 for block in encrypted_blocks]).astype(int)
        decrypted_img = decrypted_blocks.reshape(img_padded.shape)

        # Remove padding
        encrypted_img = encrypted_img[:height, :width]
        decrypted_img = decrypted_img[:height, :width]

        return img_array, encrypted_img.astype(np.uint8), decrypted_img.astype(np.uint8)
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None, None

# Get user input for the 16x16 key matrix
while True:
    key_matrix = get_user_matrix()
    if is_invertible(key_matrix):
        break
    else:
        print("The matrix is not invertible. Please enter a new matrix.")

# Encrypt and decrypt the image
original, encrypted, decrypted = encrypt_decrypt_image('frog.jpg', key_matrix)

if original is not None and encrypted is not None and decrypted is not None:
    # Display results
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
    ax1.imshow(original)
    ax1.set_title('Original')
    ax1.axis('off')
    ax2.imshow(encrypted, cmap='gray')
    ax2.set_title('Encrypted')
    ax2.axis('off')
    ax3.imshow(decrypted, cmap='gray')
    ax3.set_title('Decrypted')
    ax3.axis('off')
    plt.tight_layout()
    plt.show()

    # Verify key matrix
    print("Key Matrix:")
    print(key_matrix)
    print("\nDeterminant of Key Matrix:", np.linalg.det(key_matrix))
    print("\nInverse of Key Matrix:")
    print(np.linalg.inv(key_matrix))
else:
    print("Failed to process the image. Please check the image file and try again.")