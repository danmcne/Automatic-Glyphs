import numpy as np
from PIL import Image
import uuid
import random
import os

# Directions (N, NE, E, SE, S, SW, W, NW) as movement vectors on the grid
DIRECTIONS = {
    'N': (-1, 0),   # North
    'NE': (-1, 1),  # North-East
    'E': (0, 1),    # East
    'SE': (1, 1),   # South-East
    'S': (1, 0),    # South
    'SW': (1, -1),  # South-West
    'W': (0, -1),   # West
    'NW': (-1, -1)  # North-West
}

# Starting positions (9 central locations in the 14x14 grid)
START_POSITIONS = [
    (1, 1), (1, 7), (1, 13),  # upper-left, upper-middle, upper-right
    (7, 1), (7, 7), (7, 13),  # middle-left, middle-middle, middle-right
    (13, 1), (13, 7), (13, 13) # lower-left, lower-middle, lower-right
]

# Function to generate a glyph with random strokes
def generate_glyph_image(grid_size=(14, 14)):
    # Create an empty 14x14 grid with 0s (border will be added later)
    grid = np.zeros(grid_size, dtype=int)

    # Randomly select a starting position
    x, y = random.choice(START_POSITIONS)

    # Mark the starting position
    grid[x, y] = 1

    # Triangular distribution for the number of strokes (between 1 and 11, mode around 5-6)
    num_strokes = int(random.triangular(1, 10, 5))

    for _ in range(num_strokes):
        # Pick a random direction
        direction = random.choice(list(DIRECTIONS.values()))

        # Triangular distribution for stroke length (between 2 and 12, mode around 7)
        stroke_length = int(random.triangular(2, 14, 7))

        # Make the turtle move by approximately the chosen stroke length
        for _ in range(stroke_length):
            x, y = x + direction[0], y + direction[1]
            
            # Ensure the turtle stays within bounds (14x14 grid)
            x = min(max(x, 0), grid_size[0] - 1)
            y = min(max(y, 0), grid_size[1] - 1)

            # Draw the pen stroke (mark the grid)
            grid[x, y] = 1

    # Add a 1-pixel padding around the grid to make it 16x16
    padded_grid = np.pad(grid, pad_width=1, mode='constant', constant_values=0)

    return padded_grid

# Function to save the generated 16x16 glyph image
def save_glyph_image(image_array, save_directory='glyphs'):
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # Generate a unique filename using UUID
    filename = f"{uuid.uuid4()}.png"

    # Convert the array to an image (multiply by 255 to convert 0/1 to grayscale)
    img = Image.fromarray((image_array * 255).astype(np.uint8))

    # Save the image
    img.save(os.path.join(save_directory, filename))
    print(f"Glyph saved as {filename}")

# Generate and save multiple glyph images
def generate_and_save_glyphs(num_images=20, save_directory='glyphs'):
    for _ in range(num_images):
        glyph_image = generate_glyph_image()
        save_glyph_image(glyph_image, save_directory)

# Example usage
if __name__ == "__main__":
    # Generate and save 20 random glyph images
    generate_and_save_glyphs(num_images=20, save_directory='glyphs')

