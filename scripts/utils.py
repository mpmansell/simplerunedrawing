"""Utility functions for the build and distribution scripts.

This module provides common utility functions used by build and distribution
scripts, including command execution, file operations, and archive creation.
All functions provide formatted console output and consistent error handling.

Functions:
    run_command: Execute a subprocess command with progress reporting.
    move_file: Move/rename a file with automatic directory creation.
    create_zip: Create a zip archive from a directory with relative paths.

Example:
    >>> from scripts.utils import run_command, move_file, create_zip
    >>> # Run a command
    >>> if run_command(["python", "--version"]):
    ...     # Move a file
    ...     if move_file("src.txt", "dest/src.txt"):
    ...         # Create a zip
    ...         create_zip("dest", "archive.zip")
"""

__all__ = ["run_command", "move_file", "create_zip"]

import shutil
import subprocess
from pathlib import Path
from typing import List
from rich import print as rrprint

def run_command(cmd: List[str], description: str=""):
    """Execute a subprocess command with progress reporting.
    
    Runs a command using subprocess.run() and provides formatted console
    output including the command being executed and result status with
    visual indicators (✓/✗).
    
    Args:
        cmd: List of command arguments where the first element is the
             executable and subsequent elements are command arguments.
             Example: ["python", "--version"]
        description: Optional human-readable description of the command
                    to be printed before execution. If provided, will be
                    printed with "..." appended. Defaults to empty string.
    
    Returns:
        bool: True if the command executed successfully (return code 0),
              False if the command failed (non-zero return code).
    
    Raises:
        No exceptions are raised. All errors are caught internally and
        reported as False. Possible failure scenarios:
            - Executable not found in PATH
            - Command execution fails (non-zero exit code)
            - Subprocess communication errors
    
    Side Effects:
        - Prints command description if provided
        - Prints full command being executed
        - Prints result status with indicator (✓ or ✗)
        - Prints exit code if command fails
    
    Example:
        >>> success = run_command(["python", "--version"], "Checking Python")
        Checking Python...
        Running: python --version
        ✓ Command succeeded
        >>> success
        True
    """
    if description:
        print(f"\n{description}...")
        
    print(f"Running: {' '.join(cmd)}")
    
    result: subprocess.CompletedProcess = subprocess.run(cmd)
    if result.returncode != 0:
        rrprint(f"[bold bright_red]✗ Command failed with exit code {result.returncode}")
        return False
    
    rrprint(f"[bold bright_green]✓ Command succeeded")
    return True


def move_file(src, dst, description=""):
    """Move/rename a file with automatic parent directory creation.
    
    Moves a file from source to destination path, automatically creating
    any missing parent directories. Provides formatted console output for
    progress tracking and error reporting with visual indicators (✓/✗).
    
    Args:
        src: Source file path as str or Path object. The file must exist,
             otherwise the function returns False. Supports both absolute
             and relative paths.
        dst: Destination file path as str or Path object. Parent directories
             will be automatically created if they don't exist. If a file
             exists at the destination, it will be overwritten.
        description: Optional human-readable description of the move
                    operation to be printed before execution. If provided,
                    will be printed with "..." appended. Defaults to
                    empty string.
    
    Returns:
        bool: True if the file was successfully moved, False if the move
              operation failed for any reason.
    
    Raises:
        No exceptions are raised. All errors are caught internally and
        reported as False. Possible failure scenarios:
            - Source file does not exist
            - Insufficient permissions to read source file
            - Insufficient permissions to write to destination
            - Destination is on a different filesystem (OS-dependent)
            - Disk space exhausted
            - Invalid file path characters or length
            - Source is a directory (not a file)
    
    Side Effects:
        - Creates parent directories for destination path if needed
        - Prints operation description if provided
        - Prints success/failure status with indicator (✓ or ✗)
        - Prints error message if operation fails
        - Original source file is deleted upon successful move
    
    Example:
        >>> moved = move_file("old.txt", "new_folder/new.txt", "Moving file")
        Moving file...
        ✓ Moved old.txt to new_folder/new.txt
        >>> moved
        True
        
        >>> moved = move_file("nonexistent.txt", "dest.txt")
        ✗ Source not found: nonexistent.txt
        >>> moved
        False
    """
    src: Path = Path(src)
    dst: Path = Path(dst)
    
    if not src.exists():
        rrprint(f"[bold bright_red]✗ Source not found: {src}")
        return False
    
    if description:
        print(f"\n{description}...")
    
    try:
        dst.parent.mkdir(parents=True, exist_ok=True)

        shutil.move(str(src), str(dst))
        
        rrprint(f"[bold bright_green]✓ Moved {src.name} to {dst}")
        return True
    
    except Exception as e:
        rrprint(f"[bold bright_red]✗ Error moving {src}: {e}")
        return False


def create_zip(source_dir: Path, output_file: Path):
    """Create a compressed zip archive from a directory with relative paths.
    
    Creates a zip file from a source directory, preserving the directory
    structure relative to the source's parent. Automatically removes any
    existing zip file at the output location before creating a new one.
    Uses the `zip` command-line utility for compression.
    
    Args:
        source_dir: Source directory path to compress (Path or str).
                   Must exist and be a directory.
        output_file: Output zip file path (Path or str). Parent directories
                    will be created if needed. If file exists, it will be
                    overwritten.
    
    Returns:
        bool: True if zip file was successfully created, False otherwise.
    
    Raises:
        No exceptions are raised. Errors are caught and returned as False.
        Possible failure reasons:
            - Source directory does not exist
            - `zip` command not found in PATH
            - Insufficient permissions to read source or write output
            - Disk space issues
            - Invalid directory paths
    
    Note:
        - Temporarily changes working directory during zip creation
        - Requires `zip` command-line utility to be installed
        - Uses quiet mode (-q) and recursive mode (-r)
        - Creates relative paths in the zip (no absolute paths)
    
    Example:
        >>> from pathlib import Path
        >>> success = create_zip(Path("dist/app"), Path("dist/app.zip"))
        >>> if success:
        ...     print("Zip archive created successfully!")
    """
    source_dir: Path = Path(source_dir)
    output_file: Path = Path(output_file)
    
    if not source_dir.exists():
        rrprint(f"✗ Source directory not found: {source_dir}")
        return False
    
    try:
        # Change to the source directory
        import os
        original_cwd: str = os.getcwd()
        os.chdir(source_dir.parent)
        
        # Remove existing zip if it exists
        if output_file.exists():
            output_file.unlink()
        
        # Create zip with relative paths
        cmd: List[str] = ["zip", "-q", "-r", str(output_file.name), source_dir.name]
        result: subprocess.CompletedProcess = subprocess.run(cmd)
        
        os.chdir(original_cwd)
        
        if result.returncode != 0:
            rrprint(f"✗ Zip creation failed")
            return False
        
        rrprint(f"[bold bright_green]✓ Created zip file: {output_file}")
        return True

    except Exception as e:
        rrprint(f"[bold bright_red]✗ Error creating zip: {e}")
        return False
