#!/usr/bin/env python
"""
Build distribution script for DrawRunes.

This script automates the complete process of building a standalone,
distributable package of DrawRunes using PyInstaller:

1. Runs PyInstaller to create the onedir distribution
2. Moves data files (Runes, LICENSE, readme.md) from libs/ to root
3. Creates a compressed zip archive of the distribution

The script provides comprehensive progress reporting with clear section
headers and success/failure indicators for each phase.

Features:
    - Intelligent error handling with rollback capability
    - Optional pre-build cleanup (--clean flag)
    - Optional zip archive creation (--no-zip to skip)
    - Cross-platform path handling using pathlib
    - Detailed console output with visual indicators

Requirements:
    - Python 3.9+
    - PyInstaller (pip install pyinstaller)
    - `zip` command-line utility (built-in on Linux/Mac, install on Windows)
    - Project structure with simplerunedrawing/main.py

Usage:
    python scripts/build_dist.py              # Build with defaults
    python scripts/build_dist.py --clean      # Clean before building
    python scripts/build_dist.py --no-zip     # Build but don't create zip
    python scripts/build_dist.py --help       # Show all options

Environment Variables:
    None required. Script auto-detects project root.

Output:
    - dist/drawrunes/          : Standalone application directory
    - dist/drawrunes.zip       : Compressed archive (unless --no-zip)
    - build/                   : PyInstaller working directory (can be deleted)
    - *.spec                   : PyInstaller spec file (can be deleted)

Exit Codes:
    0 : Success
    1 : Failure (build failed, file operations failed, or zip failed)

Examples:
    # Standard build with zip
    $ python scripts/build_dist.py
    
    # Clean rebuild
    $ python scripts/build_dist.py --clean
    
    # Build without creating zip (faster, for testing)
    $ python scripts/build_dist.py --no-zip
    
    # From Makefile
    $ make distribution
    $ make build-dist-clean

See also:
    BUILD.md - Comprehensive build documentation
    scripts/utils.py - Shared utility functions
    scripts/clean.py - Artifact cleanup script
"""

import argparse
import shutil
import subprocess
import sys
import os
from pathlib import Path

from scripts.utils import run_command, move_file, create_zip
from rich import print as rrprint

display_line: str = "=" * 70
blue_line: str = f"[bold bright_blue]{display_line}[/bold bright_blue]"


def main():
    """Main entry point for the DrawRunes distribution build script.
    
    Orchestrates the complete build process:
    1. Parses command-line arguments
    2. Optionally cleans previous build artifacts
    3. Runs PyInstaller to create the distribution
    4. Reorganizes output files from libs/ to root
    5. Creates a zip archive (unless --no-zip is specified)
    
    The script provides detailed progress output with clear section headers
    and success/failure indicators for each step.
    
    Args:
        None: Arguments are parsed from command line using argparse.
    
    Returns:
        int: Exit code. 0 for success, 1 for any failure (build failed,
             file move failed, or zip creation failed).
    
    Raises:
        SystemExit: May be raised by argparse for invalid arguments or --help.
    
    Command-line Arguments:
        --clean: Remove dist/ and build/ directories before building
        --no-zip: Build distribution but don't create zip file
        --help: Show help message and exit
    
    Side Effects:
        - Creates/modifies directories: dist/, build/
        - Changes current working directory to project root
        - Prints extensive progress information to stdout
        - Calls subprocess commands (pyinstaller, zip)
        - Moves and removes files in the distribution directory
    
    Example:
        >>> import sys
        >>> exit_code = main()
        >>> sys.exit(exit_code)
    
    Environment:
        - Requires PyInstaller to be installed
        - Requires `zip` command-line utility
        - Assumes Python 3.9+ (uses pathlib, type hints)
    """
    parser = argparse.ArgumentParser(
        description="Build DrawRunes distribution with PyInstaller",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/build_dist.py              # Standard build
  python scripts/build_dist.py --clean      # Clean before building
  python scripts/build_dist.py --no-zip     # Build without creating zip
        """,
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Clean dist/ and build/ directories before building",
    )
    parser.add_argument(
        "--no-zip",
        action="store_true",
        help="Build distribution but don't create zip file",
    )

    args = parser.parse_args()

    # Get project root (parent of scripts folder)
    script_dir: Path = Path(__file__).parent
    project_root: Path = script_dir.parent

    rrprint(blue_line)
    rrprint("[bold bright_blue]DrawRunes Distribution Builder[/bold bright_blue]")
    rrprint(blue_line)
    rrprint(f"Project root: [bold bright_magenta]{project_root}[/bold bright_magenta]")

    # Change to project root
    os.chdir(project_root)

    # Clean if requested
    if args.clean:
        rrprint("\n" + blue_line)
        rrprint("[bold bright_blue]CLEANING[/bold bright_blue]")
        rrprint(blue_line)

        for folder in ["dist", "build"]:
            folder_path: Path = project_root / folder
            if folder_path.exists():
                rrprint(f"Removing [bold bright_magenta]{folder_path}[/bold bright_magenta] {folder}/...")
                shutil.rmtree(folder_path)

    # Step 1: Run PyInstaller
    rrprint("\n" + blue_line)
    rrprint("[bold bright_blue]BUILDING[/bold bright_blue]")
    rrprint(blue_line)

    pyinstaller_cmd = [
        "pyinstaller",
        "--onedir",
        "simplerunedrawing/main.py",
        "--name",
        "drawrunes",
        "--add-data",
        "../Runes/:Runes",
        "--add-data",
        "../LICENSE.md:.",
        "--add-data",
        "../readme.md:.",
        "--contents-directory",
        "libs",
        "--distpath",
        "dist/",
        "--workpath",
        "build/",
        "--specpath",
        "build/",
    ]

    if not run_command(pyinstaller_cmd, "Running PyInstaller"):
        rrprint("\n[bold bright_red]✗ Build failed!")
        return 1

    # Step 2: Move files from libs/ to root
    rrprint("\n" + blue_line)
    rrprint("[bold bright_blue]ORGANIZING FILES[/bold bright_blue]")
    rrprint(blue_line)

    base_path: Path = project_root / "dist" / "drawrunes"
    libs_path: Path = base_path / "libs"

    files_to_move: list[tuple[Path, Path, str]] = [
        (libs_path / "Runes", base_path / "Runes", "Runes directory"),
        (libs_path / "LICENSE.md", base_path / "LICENSE.md", "LICENSE.md file"),
        (libs_path / "readme.md", base_path / "readme.md", "readme.md file"),
        (Path("icons/DrawRunes.ico"), base_path / "DrawRunes.ico", "DrawRunes.ico file")
    ]

    all_moved: bool = True
    for src, dst, desc in files_to_move:
        if not move_file(src, dst, f"Moving {desc}"):
            all_moved = False

    if not all_moved:
        rrprint("\n[bold bright_red]✗ Some files could not be moved!")
        return 1

    # Step 3: Create zip if not disabled
    if not args.no_zip:
        rrprint("\n" + blue_line)
        rrprint("[bold bright_blue]CREATING ZIP ARCHIVE[/bold bright_blue]")
        rrprint(blue_line)

        zip_file = project_root / "dist" / "drawrunes.zip"
        if not create_zip(base_path, zip_file):
            rrprint("\n[bold bright_red]✗ Zip creation failed!")
            return 1
        else:
            rrprint("\n[bold bright_green]✓ Zip archive created successfully!")    

    # Success!
    rrprint("\n" + blue_line)
    rrprint("[bold bright_green]✓ BUILD COMPLETE")
    rrprint(blue_line)

    dist_path = project_root / "dist" / "drawrunes"
    rrprint(f"\nDistribution location: [bold bright_magenta]{dist_path}[/bold bright_magenta]")

    if not args.no_zip:
        zip_path = project_root / "dist" / "drawrunes.zip"
        rrprint(f"Zip archive: [bold bright_magenta]{zip_path}[/bold bright_magenta]")

    rrprint(f"\n[bold bright_blue]To run the application:[/bold bright_blue]")
    rrprint(f"  [bold bright_magenta]{dist_path / 'drawrunes.exe'}[/bold bright_magenta] --help")

    return 0


if __name__ == "__main__":
    sys.exit(main())
