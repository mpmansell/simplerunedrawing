# Simple Rune Drawing

A simple application to simulate the drawing of runes from the Elder Futhark alphabet.

Several layouts are supported, with the default being a 5 rune layout. The others are 1, 3, 7, and 9 rune layouts.

Rune images can be loaded from a custom folder, or from the default folder, but just be aware that the current implementation assumes that all rune images are the same size.

## Building

The application can be built using the `build-dist` or `build-dist-clean` targets in the make file:

- `build-dist`: Build a standalone executable distribution using PyInstaller.
  - The distribution is created in the `dist/` directory.
- `distribution`: Alias for `build-dist`.\
\
If either `build_dist` or `distribution` targets are run, you may be asked if you wish to delete previous build artifacts. If you answer 'yes', the application will be built using the default settings.

- `build-dist-clean`: Clean and rebuild the distribution.
  - This option will remove artifacts from a previous build and then build a new distribution.
  
If successful, the distribution will be available in the `dist/` directory as either:

- `DrawRunes-Installer.exe`, or
- `drawrunes.zip`.

[!NOTE] It is possible that these files may be available, ready built, as releases in the GitHub repository. It may be worth checking there first.

See 'Installation' below for instructions on how to install the application using these files.

If you wish to clean previous build artifacts independently, use the `clean` target in the make file.
  
The Windows installer can be built using the `win-installer` target in the make file.

## Installation

There are two ways to install the Windows application after it has been built:

1. Copy `DrawRunes-Installer.exe` file to the target (Windows) computer and execute as any other application installer. The uninstaller is included in installation directory (by default `C:\Program Files (x86)\DrawRunes`).

2. Extract the contents of the `drawrunes.zip` file and run the application by double-clicking the `drawrunes.exe` file.

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
    
## TODO

There are a number of improvements that are in the pipeline, including:

- full CI Integration
- Release and version management.

- More detailed development documentation

## License

The MIT License (MIT)

Copyright (c) 2023 [Mark Peter Mansell](https://github.com/mpmansell)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
