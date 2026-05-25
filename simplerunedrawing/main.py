"""Command-line interface for SimpleRuneDrawing rune divination tool.

This module provides a CLI for drawing Elder Futhark runes and optionally generating
PNG images of the results. Users can specify the number of runes to draw, request image
output, and enable verbose/debug logging for troubleshooting.

Command Line Options:
    --number, -n: Number of runes to draw. Must be one of [1, 3, 5, 7].
        Default: 5
    --output, -o: Output format for the drawn runes. If provided, generates a PNG image
        with the specified filename; otherwise outputs rune names as text.
        Default: "" (text output)
    --rune-image-folder, -r: Path to a custom folder containing the rune images. 
    --verbose, -V: Enable verbose output for debugging purposes.
        Default: False
    --debug, -D: Enable debug output for debugging purposes.
        Default: False

Examples:
    Draw 3 runes and display as text:
        python -m simplerunedrawing --number 3
    
    Draw 5 runes and save as PNG:
        python -m simplerunedrawing --number 5 --output runes.png
    
    Draw with verbose output:
        python -m simplerunedrawing --number 1 --verbose
"""

#TODO Add an option to point to a custom folder for rune image files

    
import random
import os
from typing import List, Tuple
from pathlib import Path
    
import typer

from simplerunedrawing import draw_runes, runes_to_string
from create_rune_image import create_rune_layout, get_rune_image_filename, valid_rune_layouts

__all__ = ["main"]

app = typer.Typer()

# Set uo default values for the CLI options
Valid_Numbers: List[int] = [1,3,5,7]  # Valid numbers of runes to draw

# Find default runes image folder
current_file = Path(__file__).resolve()
rune_image_folder_default = current_file.parent.parent / "Runes"  # Default path to rune images

@app.command()
def main(
    number: int = typer.Option(
        5, 
        "--number", "-n", 
        help="Number of runes to draw (must be one of 1,3,5 or 7)", 
        case_sensitive=False
    ),
    output: str = typer.Option(
        "", 
        "--output", "-o",
        help="Output format for the drawn runes. If switch applied, then a PNG image will be generated, else text."
    ),
    rune_image_folder: str = typer.Option(
        rune_image_folder_default,
        "--rune-image-folder", "-r",
        help="Path to the folder containing the rune images"
    ),
    verbose: bool = typer.Option(
        False,
        "-V", "--verbose",
        help="Enable verbose output for debugging purposes."
    ),
    debug: bool = typer.Option( 
        False,
        "-D", "--debug",
        help="Enable debug output for debugging purposes."    
    )
):

    if number not in Valid_Numbers:
        raise typer.BadParameter("Number must be one of 1,3,5 or 7")        

    if verbose:
        print(f"Number of runes to draw: {number}")
        print(f"Output format: {output}")
        print(f"Rune image folder: {rune_image_folder}")
        print(f"Verbose output: {verbose}")
        print(f"Debug output: {debug}")
        
        
    # run app
    rune_draw = runes_to_string(draw_runes(number))
    if output == "":
        print(rune_draw)
    else:
        create_rune_layout(rune_image_folder, rune_draw).save(output)


if __name__ == "__main__":
    app()