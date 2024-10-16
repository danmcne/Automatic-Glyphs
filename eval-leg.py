import numpy as np
import os
import sys
from PIL import Image

# Function to load images from a folder and convert to binary arrays
def load_images(folder_path, img_size=(16, 16)):
    images = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            img = Image.open(os.path.join(folder_path, filename)).convert('L')
            img = img.resize(img_size)
            binary_img = np.array(img) > 128  # Convert to binary (1 or 0)
            images[filename] = binary_img.astype(int)
    return images

# Function to calculate XOR-based difference between two images
def xor_difference(img1, img2):
    xor_img = np.bitwise_xor(img1, img2)
    return np.sum(xor_img) / np.size(img1)  # Proportion of different pixels

# Function to calculate reflection (horizontal flip)
def reflect_image(img):
    return np.fliplr(img)
# Function to convert binary array to a more readable format (using . for 0 and X for 1)
def format_binary_image(binary_img):
    formatted_img = []
    for row in binary_img:
        formatted_row = ''.join(['X' if pixel == 1 else '.' for pixel in row])
        formatted_img.append(formatted_row)
    return '\n'.join(formatted_img)

# Function to print binary representations of two images and show the images
def show_similar_images(img1, img2, filename1, filename2):
    print(f"\nWarning: Similar images found! Difference is less than 0.02 between {filename1} and {filename2}")
    
    # Print binary representations using . for 0 and X for 1
    print(f"Binary representation of {filename1}:")
    print(format_binary_image(img1))
    print(f"\nBinary representation of {filename2}:")
    print(format_binary_image(img2))

    # Display images using PIL's show()
    img1_display = Image.fromarray((img1 * 255).astype(np.uint8))
    img2_display = Image.fromarray((img2 * 255).astype(np.uint8))
    
    img1_display.show(title=filename1)
    img2_display.show(title=filename2)

# Function to calculate the legibility score between all pairs of images
def calculate_legibility(images, threshold=0.02):
    letters = list(images.keys())
    n = len(letters)
    differences = []

    for i in range(n):
        for j in range(i + 1, n):
            img1 = images[letters[i]]
            img2 = images[letters[j]]
            
            # XOR difference
            diff = xor_difference(img1, img2)
            
            # Reflection check
            reflected_img2 = reflect_image(img2)
            reflection_diff = xor_difference(img1, reflected_img2)
            
            # Total similarity score (adding weight for reflection)
            total_diff = diff + 0.5 * reflection_diff
            differences.append(total_diff)

            # Check if the difference is less than the threshold
            if total_diff < threshold:
                show_similar_images(img1, img2, letters[i], letters[j])

    return differences

# Function to compute summary statistics
def compute_statistics(differences):
    min_diff = np.min(differences)
    max_diff = np.max(differences)
    median_diff = np.median(differences)
    mean_diff = np.mean(differences)

    return {
        'min': min_diff,
        'median': median_diff,
        'max': max_diff,
        'mean': mean_diff
    }

# Main function to execute the evaluation
def evaluate_legibility(folder_path):
    images = load_images(folder_path)
    differences = calculate_legibility(images)
    stats = compute_statistics(differences)

    print("Legibility Statistics:")
    print(f"Min Difference: {stats['min']:.4f}")
    print(f"Median Difference: {stats['median']:.4f}")
    print(f"Mean Difference: {stats['mean']:.4f}")
    print(f"Max Difference: {stats['max']:.4f}")

# Entry point for command-line execution
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python evaluate_legibility.py <folder_path>")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    
    if not os.path.isdir(folder_path):
        print(f"Error: {folder_path} is not a valid directory.")
        sys.exit(1)

    evaluate_legibility(folder_path)

