"""Module for creating composite rune image layouts.

This module provides functionality for working with individual rune PNG images and
combining them into composite layouts. It supports creating grid arrangements for
1, 3, 5, and 7 rune configurations, commonly used in rune divination spreads.

Functions:
    get_rune_image_filename: Generate the file path for a rune's image file.
    create_rune_layout: Combine multiple rune images into a composite layout.

Constants:
    valid_rune_layouts: List of valid rune counts for layout generation.
    rune_image_folder: Path to the folder containing the rune images
"""

from PIL import Image
import os
from typing import List


__all__ = ["create_rune_layout", "get_rune_image_filename", "valid_rune_layouts", "expected_rune_filenames"]


# List of expected filenames for icons
expected_rune_filenames: List[str] = [
    "Ansuz.png",  "Beorc.png",   "Daeg.png",  "Ehwaz.png", "Eiwaz.png",    "Eohl.png",  "Fehu.png",  "Gifu.png", 
    "Hagall.png", "Ing.png",     "Isa.png",   "Jera.png",  "Kenaz.png",    "Lagaz.png", "Mannaz.png", "Nied.png", 
    "Othel.png",  "Perdhro.png", "Raido.png", "Sigel.png", "Thurisaz.png", "Tir.png",   "Uruz.png",   "Wunjo.png", 
    "reversed_Ansuz.png",    "reversed_Beorc.png",   "reversed_Daeg.png",  "reversed_Ehwaz.png", 
    "reversed_Eiwaz.png",    "reversed_Eohl.png",    "reversed_Fehu.png",   "reversed_Gifu.png", 
    "reversed_Hagall.png",   "reversed_Ing.png",     "reversed_Isa.png",    "reversed_Jera.png", 
    "reversed_Kenaz.png",    "reversed_Lagaz.png",   "reversed_Mannaz.png", "reversed_Nied.png", 
    "reversed_Othel.png",    "reversed_Perdhro.png", "reversed_Raido.png",  "reversed_Sigel.png", 
    "reversed_Thurisaz.png", "reversed_Tir.png",     "reversed_Uruz.png",   "reversed_Wunjo.png" ]

# Valid rune layouts
valid_rune_layouts = [1,3,5,7]

rune_image_folder: str = r"Runes"  # Default path to rune images - this can be overridden by the CLI option in main.py

def get_rune_image_filename(name: str) -> str:
    """Generate the file path for a rune image.
    
    Constructs the full file path to a rune's PNG image file based on the rune name.
    
    Args:
        name: The name of the rune (e.g., "Fehu", "Reversed Ansuz").
        
    Returns:
        The full file path to the rune's PNG image file.
    """
    return f"{rune_image_folder}/{name}.png"

def create_rune_layout(_rune_image_folder: str, runes: list[str]) -> Image.Image:
    """Create a composite image layout of runes.
    
    Loads individual rune PNG images and arranges them in a grid layout based on 
    the total number of runes. Supports layouts for 1, 3, 5, and 7 runes with 
    predefined positions.
    
    Args:
        _rune_image_folder: Path to the folder containing the rune images.
        runes: A list of rune names (strings) to include in the layout.
               Must contain exactly 1, 3, 5, or 7 runes.
        
    Returns:
        A PIL Image object with RGBA transparency containing the composite layout
        of the rune images arranged according to the layout rules.
        
    Raises:
        ValueError: If the number of runes is not one of [1, 3, 5, 7].
        ValueError: If any rune image file is not found or cannot be loaded.
    """
    global rune_image_folder
    rune_image_folder = _rune_image_folder
    
    number_of_runes: int = len(runes)
    
    # Validate number of runes
    if not(number_of_runes in valid_rune_layouts):
        raise ValueError("Invalid number of runes for the layout generation.")
    
    # Validate that all runes have corresponding image files
    missing_images: List[str] = []  # List to track runes that do not have corresponding images
    rune_images: List = []  # List to store the image objects of the rune images
    
    # Load rune images and check for missing ones
    for rune in runes:
        rune_image_file = get_rune_image_filename(rune)
        try:
            rune_images.append(Image.open(rune_image_file))
        except FileNotFoundError, Exception:
                missing_images.append(rune)
        
    if missing_images:
        raise ValueError(f"One or more runes do not have corresponding images: {missing_images}")
    
    w, h = rune_images[0].size  # Assuming all images are the same size
    
    # pyrefly: ignore [missing-attribute]
    rune_images = [img.resize((w, h), Image.LANCZOS ) for img in rune_images]  # Ensure all images are the same size for consistent layout
    
    # Create output image with transparent background depending on the number of runes
    output_size = [(w,h), (0,0), (3*w,h), (0,0), (3*w, 3*h), (0,0), (6*w, 2*h)][number_of_runes-1] 
    out = Image.new("RGBA", output_size, (0, 0, 0, 0))
    
    match number_of_runes:
        case 1:
            out.paste(rune_images[0], (0,0))  # Center
        case 3:
            out.paste(rune_images[0], (0, 0))   # Left
            out.paste(rune_images[1], (w, 0))   # Center
            out.paste(rune_images[2], (2*w, 0)) # Right
        case 5: 
            out.paste(rune_images[0], (0,     h))   # Left
            out.paste(rune_images[1], (w,     h))   # Center
            out.paste(rune_images[2], (2*w,   h))   # Right
            out.paste(rune_images[3], (w,     0))   # Top
            out.paste(rune_images[4], (w,   2*h))   # Bottom
        case 7:
            out.paste(rune_images[0], (0,     0)) 
            out.paste(rune_images[1], (w,     0)) 
            out.paste(rune_images[2], (2*w,   0)) 
            out.paste(rune_images[3], (3*w,   0))  
            out.paste(rune_images[4], (4*w,   0))
            out.paste(rune_images[5], (5*w,   0))
            out.paste(rune_images[6], (int(2.5*w),   h))
        case _:
            raise ValueError(f"Invalid number of runes {number_of_runes} for the layout generation.")
                            
    return out

