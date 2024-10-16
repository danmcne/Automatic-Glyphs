# Glyph Generator & Legibility Checker

This repository contains two Python scripts: one for generating random glyphs and another for evaluating the legibility and similarity of glyph images.

## Features

1. **Glyph Generator**: Generates random 16x16 glyph images using a turtle-like drawing mechanism on a 14x14 grid with padding.
2. **Legibility Checker**: Evaluates a set of 16x16 glyph images for similarity using XOR-based image comparisons. Also checks for potential symmetry by comparing each glyph with its reflection.

## Prerequisites

- Python 3.x
- The following Python libraries:
  - `numpy`
  - `Pillow` (PIL)

Install the necessary dependencies with:

```bash
pip install numpy pillow
```

## 1. Glyph Generator

This script generates a specified number of random glyphs and saves them as 16x16 PNG images.

### Usage

```bash
python3 gen-glyph.py
```

### Parameters

- `num_images`: The number of glyph images to generate (default: 20).
- `save_directory`: The directory where generated glyphs will be saved (default: `glyphs/`).

### Example

```bash
python3 gen-glyph.py
```

This will generate 20 glyphs and save them as `.png` files in the `glyphs/` folder.

### Customization

- The turtle starts at one of nine central locations on a 14x14 grid and randomly moves in one of 8 directions (N, NE, E, SE, S, SW, W, NW).
- The number of strokes and stroke lengths are drawn from a triangular distribution:
  - Strokes: Between 1 and 11 (mode around 6).
  - Stroke length: Between 2 and 12 pixels (mode around 7).

## 2. Legibility Checker

This script evaluates a folder of 16x16 glyph images for legibility by calculating the pixel-wise difference between each pair of glyphs using XOR. It also checks for symmetry by comparing glyphs to their mirrored versions.

### Usage

```bash
python3 eval-leg.py <folder_path>
```

### Parameters

- `<folder_path>`: The path to the folder containing the glyph images to check.

### Example

```bash
python3 eval-leg.py glyphs/
```

### Output

- The script will print the similarity score between each pair of glyphs. If two glyphs are highly similar (difference less than 0.1), it will display both images in the terminal as binary representations.
- The score reflects the percentage of different pixels between two images, with mirrored glyphs being weighted at 0.5 for symmetry checking.

## Folder Structure

```
.
├── gen-glyph.py        # Glyph generation script
├── eval-leg.py    # Glyph similarity checker script
├── glyphs/                   # Folder where generated glyphs are saved
└── README.md                 # This readme file
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
