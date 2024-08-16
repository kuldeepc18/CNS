from PIL import Image
import matplotlib.pyplot as plt

class ShiftCypher:
    def __init__(self, key):
        self.key = key

    def encrypt(self, para):
        return "".join([chr((ord(x) + self.key) % 128) for x in para])

    def decrypt(self, encrypted):
        return "".join([chr((ord(x) - self.key) % 128) for x in encrypted])


class ShiftCypherInts:
    def __init__(self, key):
        self.key = key

    def process_pixel(self, pixel, operation):
        r, g, b = pixel
        if operation == 'encrypt':
            return ((r + self.key) % 256, (g + self.key) % 256, (b + self.key) % 256)
        elif operation == 'decrypt':
            return ((r - self.key) % 256, (g - self.key) % 256, (b - self.key) % 256)
        else:
            raise ValueError("Operation must be 'encrypt' or 'decrypt'.")

    def encrypt(self, pixel):
        return self.process_pixel(pixel, 'encrypt')

    def decrypt(self, pixel):
        return self.process_pixel(pixel, 'decrypt')


def ascii_cypher():
    key = int(input("Enter Key: "))
    cypher = ShiftCypher(key)

    para = input("Enter Text: ")
    encrypted = cypher.encrypt(para).upper()
    print(f"Encrypted: {encrypted}")
    decrypted = cypher.decrypt(encrypted).lower()
    print(f"Decrypted: {decrypted}")


def apply_cipher(image, key, operation):
    cypher = ShiftCypherInts(key)
    pixels = list(image.getdata())
    if operation == 'encrypt':
        new_pixels = [cypher.encrypt(pixel) for pixel in pixels]
    elif operation == 'decrypt':
        new_pixels = [cypher.decrypt(pixel) for pixel in pixels]
    else:
        raise ValueError("Operation must be 'encrypt' or 'decrypt'.")

    new_image = Image.new(image.mode, image.size)
    new_image.putdata(new_pixels)
    return new_image


def plot_histograms(image, title, ax):
    # Ensure the image is in RGB mode
    image = image.convert('RGB')
    
    # Get image data
    pixels = list(image.getdata())
    r_vals, g_vals, b_vals = zip(*pixels)
    
    # Create histograms
    ax.hist(r_vals, bins=256, color='red', alpha=0.6, label='Red Channel')
    ax.hist(g_vals, bins=256, color='green', alpha=0.6, label='Green Channel')
    ax.hist(b_vals, bins=256, color='blue', alpha=0.6, label='Blue Channel')
    
    # Set x-axis limits to zoom in (e.g., 0 to 128)
    ax.set_xlim([0, 50])  # Adjust this range as needed
    ax.set_title(title)
    ax.set_xlabel('Pixel Value')
    ax.set_ylabel('Frequency')
    ax.legend()


def show_images(original, encrypted, decrypted):
    # Create a matplotlib figure with subplots
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    
    # Plot images
    axes[0, 0].imshow(original)
    axes[0, 0].set_title("Original Image")
    axes[0, 0].axis('off')

    axes[0, 1].imshow(encrypted)
    axes[0, 1].set_title("Encrypted Image")
    axes[0, 1].axis('off')

    axes[0, 2].imshow(decrypted)
    axes[0, 2].set_title("Decrypted Image")
    axes[0, 2].axis('off')

    # Plot histograms
    plot_histograms(original, 'Histogram of Original Image', axes[1, 0])
    plot_histograms(decrypted, 'Histogram of Decrypted Image', axes[1, 1])
    
    # Leave the last subplot empty or use it for other purposes
    axes[1, 2].axis('off')

    plt.tight_layout()
    plt.show()
    print("Images and histograms visible")


def image_cypher():
    key = int(input("Enter Key: "))
    try:
        original_image = Image.open("mickey.png")  # Update this with the correct filename
    except FileNotFoundError:
        print("Error: The image file 'mickey.png' was not found.")
        return

    encrypted_image = apply_cipher(original_image, key, 'encrypt')
    decrypted_image = apply_cipher(encrypted_image, key, 'decrypt')

    encrypted_image.save("encrypted_image.jpg")
    decrypted_image.save("decrypted_image.jpg")
    print("Images have been processed and saved.")

    # Show images and histograms using matplotlib
    show_images(original_image, encrypted_image, decrypted_image)


if __name__ == "__main__":
    image_cypher()
