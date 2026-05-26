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

__version__ = '0.1.0'
    
import random
import os
import sys
from typing import List, Tuple
from pathlib import Path
from rich import print as rrprint
    
import typer

from simplerunedrawing import draw_runes, runes_to_string
from create_rune_image import create_rune_layout, get_rune_image_filename, valid_rune_layouts, expected_rune_filenames 

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
    version: bool = typer.Option(
        False,
        "--version", "-v",
        help="Show the version of the application and exit."
    ),
    debug: bool = typer.Option( 
        False,
        "-D", "--debug",
        help="Enable debug output for debugging purposes."    
    )
):

    if number not in Valid_Numbers:
        raise typer.BadParameter("Number must be one of 1,3,5 or 7")   

    # Get list of rune image filenames in the specified folder for validation and debugging purposes
    rune_image_file_names = [f.name for f in Path(rune_image_folder).glob("*.png")]
    
    # Check for missing image files
    expected_rune_filenames_set = set(expected_rune_filenames)
    missing_files = expected_rune_filenames_set - set(rune_image_file_names)
    if missing_files:
        rrprint("=" * 70)
        rrprint(f"[bold red]Missing rune image files: [/bold red]{missing_files}.\n")
        rrprint("[bold red]Please ensure all expected rune images are present in the folder before restarting.")
        sys.exit(1)   
        
    if version:
        rrprint("DrawRunes Version {version}".format(version=__version__))
        sys.exit(0)

    if verbose:
        print(f"Number of runes to draw: {number}")
        print(f"Output format: {output}")
        print(f"Rune image folder: {rune_image_folder}")
        print(f"Verbose output: {verbose}")
        print(f"Debug output: {debug}")
        
    if debug:
        print("=" * 70)
        print("Printing debug information about the environment and rune image folder for troubleshooting purposes.")
        print("=" * 70)

        print(f"Current working directory: {os.getcwd()}")
        print(f"Rune image folder: {rune_image_folder}")
        print(f"Valid rune layout combinations: {valid_rune_layouts}")
        
        # Print the contents of the rune image folder
        print("=" * 70)

        print(f"There are {len(rune_image_file_names)} images in the folder {rune_image_file_names}")
        print("=" * 70)
        
        print("\n\n")
    
    # run app
    rune_draw = runes_to_string(draw_runes(number))
    if output == "":
        print(rune_draw)
    else:
        create_rune_layout(rune_image_folder, rune_draw).save(output)


if __name__ == "__main__":
    app()