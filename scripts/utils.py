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

__all__ = [
    "run_command",
    "move_file",
    "copy_file",
    "create_zip",
    "remove_files_and_directories",
    "remove_artifacts",
    "remove_path",
    "unlink_file",
    "unlink_directory",
    "inform_intention",
    "inform_success",
    "inform_failure",
    "inform_note",
    "inform_error",
    "inform_info",
    "inform_warning",
    "inform_debug",
    "print_subheader",
    "print_title",
    "print_subheader",
    "colour_filename",
]

import os
import shutil
import subprocess
from pathlib import Path
from typing import List, Union

from rich import print as rrprint


def run_command(cmd: List[str], description: str = ""):
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
        inform_intention(f"{description}...")

    inform_intention(f"Running: [bold bright_cyan]{' '.join(cmd)}[/bold bright_cyan]")

    result: subprocess.CompletedProcess = subprocess.run(cmd)
    if result.returncode != 0:
        inform_failure(
            f"Command failed with exit code [bold bright_red]{result.returncode}[/bold bright_red]"
        )
        return False

    inform_success(f"Command succeeded")
    return True


def move_file(src: Union[Path | str], dest: Union[Path | str], description=""):
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

    source: Path = Path(src)
    destination: Path = Path(dest)

    if description:
        inform_intention(f"\n{description}...")

    if not source.exists():
        inform_failure(f"Source not found: {src}")
        return False
    else:
        try:
            # Create parent directories for destination if they don't exist
            destination.parent.mkdir(parents=True, exist_ok=True)

            # Finally attempt to move the file
            if shutil.move(source, destination):
                inform_success(
                    f"{colour_filename(source.name)} file moved successfully!"
                )
                return True
            else:
                inform_failure(
                    f"{colour_filename(source.name)} file could not be moved!"
                )
                return False

        except Exception as e:
            inform_failure(
                f"[bold bright_red]✗ Unanticipated Error while moving {colour_filename(source.name)} to {colour_filename(destination.name)}: [/bold red]{e.__new__}[/bold red]"
            )
            return False


def copy_file(src: Union[Path | str], dest: Union[Path | str], description=""):
    """
    Copy a file from source to destination.

    Args:
        src: Source file path (Path or str).
        dest: Destination file path (Path or str).
        description: Optional description for the operation.

    Returns:
        bool: True if the file was copied successfully, False otherwise.
    """
    source: Path = Path(src)
    destination: Path = Path(dest)

    if description:
        inform_intention(f"{description}...")

    inform_info(
        f"Copying {colour_filename(source.name)} to {colour_filename(destination.name)}"
    )

    if not source.exists():
        inform_failure(f"Source not found: {src}")
        return False
    else:
        try:
            if shutil.copy2(source, destination):
                inform_success(
                    f"{colour_filename(source.name)} file copied successfully!"
                )
                return True
            else:
                inform_failure(
                    f"{colour_filename(source.name)} file could not be copied!"
                )
                return False

        except Exception as e:
            inform_failure(
                f"Unanticipated Error while copying {colour_filename(source.name)} to {colour_filename(destination.name)}: {e.__new__}"
            )
            return False

    return True


def unlink_file(path: Union[Path | str]):
    """Delete a file at the specified path.

    Args:
        path: Path to the file to be deleted (Path or str).

    Returns:
        bool: True if the file was deleted successfully, False otherwise.
    """
    try:
        Path(path).unlink()
        inform_success(f"{colour_filename(Path(path).name)} file deleted successfully!")
        return True
    except Exception as e:
        inform_failure(
            f"Unanticipated Error while deleting {colour_filename(Path(path).name)}: {e.__new__}"
        )
        return False


def unlink_directory(path: Union[Path | str]):
    """Delete a directory at the specified path.

    Args:
        path: Path to the directory to be deleted (Path or str).

    Returns:
        bool: True if the directory was deleted successfully, False otherwise.
    """
    try:
        Path(path).rmdir()
        inform_success(
            f"{colour_filename(Path(path).name)} directory deleted successfully!"
        )
        return True
    except Exception as e:
        inform_failure(
            f"Unanticipated Error while deleting {colour_filename(Path(path).name)}: {e.__new__}"
        )
        return False


def remove_path(path: Union[Path | str], verbose: bool = True):
    """Delete a file or directory at the specified path.

    Args:
        path: Path to the file or directory to be removed (Path or str).
        verbose: If True, print information about the removal.

    Returns:
        bool: True if the file or directory was removed successfully, False otherwise.
    """

    try:
        if Path(path).is_file():
            Path(path).unlink()
            if verbose:
                inform_success(
                    f"{colour_filename(Path(path).name)} file removed successfully!"
                )
        else:
            if Path(path).is_dir():
                shutil.rmtree(path)
                if verbose:
                    inform_success(
                        f"{colour_filename(Path(path).name)} directory removed successfully!"
                    )
    except Exception as e:
        inform_failure(
            f"Unanticipated Error while removing {colour_filename(Path(path).name)}: {e.__new__}"
        )
        return False

    return True


def remove_files_and_directories(
    paths: Union[List[Path] | List[str] | List[Union[Path, str]]], verbose: bool = True
):
    """Delete multiple files or directories at the specified paths.

    Args:
        paths: List of paths to files or directories to be removed (List of Path or str).
        verbose: If True, print information about each removal.

    Returns:
        bool: True if all files and directories were removed successfully, False if any removal failed.

    Note:
        - This function attempts to remove all specified paths and reports success or failure for each.
        - The function returns False if any individual removal fails, but it will still attempt to remove all paths regardless of individual failures.
        - The function returns True if all paths are successfully removed.

        This function also has an alias `remove_artifacts` for readability in the context of cleaning build artifacts.

    Example:
        >>> paths_to_remove = ["file1.txt", "dir1", "file2.txt"]
        >>> success = remove_files_and_directories(paths_to_remove)  # Returns True if all removed, False if any failed or could not be removed


    """
    all_successful: bool = True

    for path in paths:
        if verbose:
            inform_intention(f"Removing {colour_filename(Path(path).name)}...")

        if not remove_path(path, verbose=verbose):
            all_successful = False
            inform_failure(f"Failed to remove {colour_filename(Path(path).name)}")
        else:
            inform_success(f"Removed {colour_filename(Path(path).name)} successfully!")
    if not all_successful:
        if verbose:
            inform_failure(f"Some items could not be removed. See above for details.")
        return False

    return all_successful


# alias for remove_files_and_directories for readability in context
remove_artifacts = remove_files_and_directories


def create_zip(
    source_dir: Union[Path | str], output_file: Union[Path | str]
):  # source_dir: Path, output_file: Union[Path|str]):
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

    source_dir = Path(source_dir)
    output_file = Path(output_file)

    inform_intention(
        f"Creating zip archive from {colour_filename(source_dir.name)} to {colour_filename(output_file.name)}"
    )

    if not source_dir.exists():  # Check if source directory exists
        inform_failure(f"Source directory not found: {source_dir}")
        return False

    if (
        output_file.exists()
    ):  # Remove existing zip if it exists, but only after confirming the source directory exists (above)
        try:
            output_file.unlink()
        except Exception as e:
            inform_failure(f"Failed to remove existing zip file: {e}")
            return False

        inform_success(
            f"Removed existing zip file: {colour_filename(output_file.name)}"
        )

    if (
        not output_file.parent.exists()
    ):  # Create parent directory path if it doesn't exist
        inform_info(
            f"Output directory not found; creating {colour_filename(output_file.parent.name)}"
        )

        try:
            output_file.parent.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            inform_failure(
                f"Failed to create output directory: [bold red]{e}[/bold red]"
            )
            return False

    try:
        # Change to the source directory (`pushd`)
        original_cwd: str = os.getcwd()
        os.chdir(source_dir.parent)
    except Exception as e:
        inform_failure(f"Failed to change directory to source parent: [bold red]{e}")
        inform_failure(f"Cannot create zip archive without access to source directory.")
        return False

    try:  # Create zip with relative paths
        cmd: List[str] = ["zip", "-q", "-r", str(output_file.name), source_dir.name]
        result: subprocess.CompletedProcess = subprocess.run(cmd)

        if result.returncode != 0:
            inform_failure(
                f"Zip creation failed with exit code [bold red]{result.returncode}[/bold red]."
            )
            return False

        os.chdir(original_cwd)  # `popd`

    except Exception as e:
        inform_failure(f"Error creating zip: {e}")
        return False

    inform_success(f"Created zip file: {output_file}")
    return True


##############################################################################
# Process message (and logging?) utilities for build tools
##############################################################################


def inform_success(message: str):
    """Print a success message with a green tick."""
    rrprint(f"[bold bright_green]✓ {message}")


def inform_failure(message: str):
    """Print a failure message with a red cross."""
    rrprint(f"[bold bright_red]✗ {message}")


def inform_warning(message: str):
    """Print a warning message with a yellow exclamation mark."""
    rrprint(f"[bold bright_yellow]⚠ {message}")


def inform_info(message: str):
    """Print an informational message with a blue info symbol."""
    rrprint(f"[bold bright_blue]ℹ {message}")


def inform_debug(message: str):
    """Print a debug message with a cyan debug symbol."""
    rrprint(f"[bold bright_cyan]🐛 {message}")


def inform_intention(message: str):
    """Print a message with no annotation unless already embedded in the message."""
    rrprint(f"{message}")


def inform_note(message: str):
    """Print a note message with a magenta note symbol."""
    rrprint(f"[bold bright_magenta]📝 {message}")


def inform_error(message: str):
    """Print an error message with a red cross."""
    rrprint(f"[bold bright_red]✗ {message}")


def print_title(message: str):
    """Print a title message with blue lines above and below."""
    blue_line = "[bold bright_blue]" + ("=" * len(message)) + "[/bold bright_blue]"
    rrprint("\n" + blue_line)
    rrprint(f"[bold bright_blue]{message}[/bold bright_blue]")
    rrprint(blue_line)
    rrprint("\n")


def print_subheader(message: str):
    """Print a subheader message with green lines above and below."""
    green_line = "[bold bright_green]" + ("─" * len(message)) + "[/bold bright_green]"
    rrprint("\n" + green_line)
    rrprint(f"[bold bright_green]{message}[/bold bright_green]")
    rrprint(green_line)
    rrprint("\n")


def colour_filename(filename: str):
    """Return a filename string colored in magenta."""
    return f"[bold bright_magenta]{filename}[/bold bright_magenta]"
