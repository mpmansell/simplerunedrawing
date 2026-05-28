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
import os
import sys
from pathlib import Path
from typing import List, Union

from rich import print as rrprint

from scripts.utils import (
    copy_file,
    create_zip,
    inform_failure,
    inform_info,
    inform_intention,
    inform_success,
    move_file,
    print_title,
    remove_files_and_directories,
    remove_path,
    run_command,
)

version: str = "1.0.0"


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

    print_title("DrawRunes Distribution Builder")
    inform_intention("Initializing build process...")
    inform_info(
        f"Project root: [bold bright_magenta]{project_root}[/bold bright_magenta]"
    )

    # Change to project root
    try:
        os.chdir(project_root)
        inform_success(
            f"Changed working directory to project root: [bold bright_magenta]{project_root}[/bold bright_magenta]"
        )
    except OSError as e:
        inform_failure(f"Failed to change working directory to project root: {e}")
        return 1

    # Clean up old distribution files if requested
    if args.clean:
        inform_intention("\nCleaning build artifacts...")

        all_artifacts: Union[list[str] | List[Path]] = ["dist", "build"]

        # Strip out any artifacts that do not exist to avoid unnecessary error messages during cleanup
        existing_artifacts: list[Path] = [
            Path(f) for f in all_artifacts if (project_root / f).exists()
        ]

        if not remove_files_and_directories(existing_artifacts, verbose=True):
            inform_failure(f"Some artifacts could not be deleted.")
            return 1

    # Run PyInstaller
    print_title("Building distribution with PyInstaller")

    pyinstaller_cmd = [
        "pyinstaller",
        "--onedir",
        "DrawRunes/main.py",
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
        inform_failure("Build failed!")
        return 1

    inform_success("PyInstaller build completed successfully!")
    
    inform_success("Windows installer created successfully!")

    # Move files from libs/ to root
    #
    # Note: PyInstaller's `--contents-directory` option places additional data files in a `libs/` subdirectory within the distribution.
    # We need to move these files back to the root of the distribution for the application to function correctly. This step ensures the final directory structure is correct for end-users.
    #
    # TODO: Consider modifying the PyInstaller spec file to place these files directly in the root of the distribution, eliminating the need for this post-processing step. This would simplify the build process and reduce potential points of failure.
    # TODO: Read the `pyinstaller` manual more comprehensively and see if there's a better way to do this :)

    print_title("Move files from libs/ to root")

    base_path: Path = project_root / "dist" / "drawrunes"
    libs_path: Path = base_path / "libs"

    files_to_move: list[tuple[Path, Path, str]] = [
        (libs_path / "Runes", base_path / "Runes", "Runes directory"),
        (libs_path / "LICENSE.md", base_path / "LICENSE.md", "LICENSE.md file"),
        (libs_path / "readme.md", base_path / "readme.md", "readme.md file"),
    ]

    all_moved: bool = True
    for src, dst, description in files_to_move:
        if not move_file(src, dst, f"Moving {description}"):
            inform_failure(f"Failed to move {description}")
            all_moved = False

    if not all_moved:
        inform_failure("Some files could not be moved!")
        return 1

    # Copy the icon file to `dist/`
    destination: Path = base_path / "DrawRunes.ico"
    source: Path = project_root / "icons" / "DrawRunes.ico"

    if not copy_file(source, destination, description=""):
        inform_failure("Failed to copy icon file!")
        return 1

    inform_success("Icon file copied successfully!")        


    # Create installer executable using Inno Setup (Windows only)
    print_title("Building Windows installer with Inno Setup")

    inno_cmd: List[str] = ["makensis", "installer.nsi"]

    if not run_command(inno_cmd, "Running Inno Setup"):
        inform_failure("Windows installer build failed!")
        return 1
    
    inform_success("Windows installer created successfully!")
    
    # # Move the generated installer executable to the dist/ directory

    # if not move_file( src= project_root / "build" / "DrawRunes-Installer.exe",
    #                   dest= project_root / "dist" / "DrawRunes-Installer.exe",
    #                   description= "Installer executable"):
    #     inform_failure("Failed to move installer executable!")
    #     return 1
    # else:
    #     inform_success("Installer executable moved successfully!")

    # Create zip if not disabled
    if not args.no_zip:
        print_title("Creating Zip archive")

        zip_file = project_root / "dist" / "drawrunes.zip"

        if not create_zip(base_path, zip_file):
            inform_failure("Zip creation failed!")
            return 1
        else:
            inform_success("Zip archive created successfully!")

    # Build Success!
    inform_success("Build completed successfully!")

    dist_path = project_root / "dist" / "drawrunes"
    inform_info(
        f"Distribution location: [bold bright_magenta]{dist_path}[/bold bright_magenta]"
    )

    if not args.no_zip:
        zip_path = project_root / "dist" / "drawrunes.zip"
        inform_info(
            f"Zip archive: [bold bright_magenta]{zip_path}[/bold bright_magenta]"
        )

    inform_info(f"\nTo run the application:")
    inform_info(
        f"  [bold bright_magenta]{dist_path / 'drawrunes.exe'}[/bold bright_magenta] --help"
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
