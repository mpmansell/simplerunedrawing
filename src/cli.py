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

import random
from typing import List, Tuple

import typer

from simplerunedrawing import draw_runes, runes_to_string



app = typer.Typer()

Valid_Numbers: List[int] = [1,3,5,7]

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
        print(f"Verbose output: {verbose}")
        print(f"Debug output: {debug}")
        
    # run app
    if output == "":
        print(runes_to_string(draw_runes(number)))
    else:
        raise NotImplementedError("Output format other than text is not yet implemented.")
    

if __name__ == "__main__":
    app()