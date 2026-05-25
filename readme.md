# Simple Rune Drawing

A simple application to simulate the drawing of runes from the Elder Futhark alphabet.

Several layouts are supported, with the default being a 5 rune layout. The others are 1, 3, 7, and 9 rune layouts.

Rune images can be loaded from a custom folder, or from the default folder, but just be aware that the current implementation assumes that all rune images are the same size.

## Installation

To be done

## Usage

The following command line options are available:

    --number, -n: Number of runes to draw. Must be one of [1, 3, 5, 7]. Default is 5.
    
    --output, -o: Output format for the drawn runes. If provided, generates a PNG image with the specified filename; otherwise outputs rune names as text. Default is "" (text output).
    
    --folder, -f: Folder containing rune images. Default is "runes".    
    
    --verbose, -V: Enable verbose output for debugging purposes. Default is False.    
    
    --help, -h: Display this help message.    
    --version, -v: Display version information.

## Examples

    python src/simplerunedrawing.py -n 1 -o test.png
    python src/simplerunedrawing.py -n 5
    
    python src/simplerunedrawing.py --number 1 --output test.png
    python src/simplerunedrawing.py --number 5

    python src/simplerunedrawing.py -n 1 -o test.png -f custom_folder
    python src/simplerunedrawing.py -n 5 -f custom_folder
    
## License

The MIT License (MIT)

Copyright (c) 2023 [Mark Peter Mansell](https://github.com/mpmansell)
