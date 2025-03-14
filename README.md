# IMG-BG-REMOVE

A Python tool to automatically remove image backgrounds and create transparent PNG files.

## Features

- Automatically detects and removes background colors
- Supports multiple image formats (JPG, JPEG, PNG, WEBP)
- Processes all images in the `src` directory
- Creates transparent PNG versions of your images

## Requirements

- Python 3.x
- Pillow (PIL) library

## Installation

1. Install Python if you haven't already
2. Install the required dependency:
```sh
pip install Pillow
```

## Usage

1. Place your images in the `src` directory
2. Run the script:
```sh
python bot.py
```
3. Find your processed images in the same directory with '_transparent' suffix

## How it works

The script works by:
1. Detecting the background color from the top-left pixel
2. Converting matching colors (within tolerance) to transparent
3. Saving the result as a PNG with transparency

## Example

Input: `image.webp` → Output: `image_transparent.png`
