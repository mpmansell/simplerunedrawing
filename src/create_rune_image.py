from PIL import Image
import os
from typing import List


__all__ = ["create_rune_layout", "get_rune_image_filename", "valid_rune_layouts"]

# Valid rune layouts
valid_rune_layouts = [1,3,5,7]

def get_rune_image_filename(name: str) -> str:
    Rune_Images = r"C:/Users/markm/Documents/Development/Projects/Software Projects/Runes/simplerunedrawing/Runes"
    
    return f"{Rune_Images}/{name}.png"

def create_rune_layout(runes: list[str]) -> Image.Image:
    
    number_of_runes: int = len(runes)
    
    # Validate number of runes
    if not(number_of_runes in valid_rune_layouts):
        raise ValueError("Invalid number of runes for the layout generation.")
    
    # Validate that all runes have corresponding image files
    missing_images: List[str] = []  # List to track runes that do not have corresponding images
    rune_images: List[Image.Image] = []  # List to store the image objects of the rune images
    
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
    # TODO: Add code to resize images if they are not the same size, or raise an error if they cannot be resized to a common size.
    
    
    # Create output image with transparent background depending on the number of runes
    output_size = [(w,h), (3*w,h), (3*w, 3*h), (6*w, 2*h)][number_of_runes] 
    out = Image.new("RGBA", output_size, (0, 0, 0, 0))
    
    match number_of_runes:
        case 1:
            out.paste(rune_images[0], (0,0))  # Center
        case 3:
            out.paste(rune_images[0], (0, h))   # Left
            out.paste(rune_images[1], (w, h))   # Center
            out.paste(rune_images[2], (2*w, h)) # Right
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
            out.paste(rune_images[6], (int(3.5*w),   h))
        case _:
            raise ValueError(f"Invalid number of runes {number_of_runes} for the layout generation.")
                            
    return out

