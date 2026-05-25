#!/usr/bin/env python
"""
Clean build artifacts from the DrawRunes project.

This script safely removes build artifacts including:
- dist/ directory
- build/ directory
- DrawRunes-Installer.exe
- *.spec files (PyInstaller spec files)

Usage:
    python clean.py                 # Show what will be removed (dry run)
    python clean.py --force         # Actually remove the files
    python clean.py --help          # Show help
    python clean.py -f              # Short form of --force

Examples in Makefile:
    clean:
        python clean.py --force
    
    clean-dry:
        python clean.py
"""

import argparse
import shutil
import sys
from pathlib import Path
from rich import print as rrprint


def main():
    parser = argparse.ArgumentParser(
        description="Clean build artifacts from the DrawRunes project",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python clean.py              # Dry run - show what would be deleted
  python clean.py --force      # Actually delete the artifacts
  python clean.py -f           # Short form
        """,
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Actually delete files. Without this flag, only shows what would be deleted.",
    )

    args = parser.parse_args()

    # Get project root
    project_dir = Path(__file__).parent.parent.resolve()

    # Define artifacts to clean
    artifacts = [
        project_dir / "dist",
        project_dir / "build",
        project_dir / "DrawRunes-Installer.exe",
    ]

    # Also find and include any .spec files
    spec_files = list(project_dir.glob("*.spec"))

    all_artifacts = artifacts + spec_files

    # Filter to only existing items
    existing_artifacts = [item for item in all_artifacts if item.exists()]

    if not existing_artifacts:
        print("No build artifacts found to clean.")
        return 0

    print("Build artifacts to be removed:")
    print("-" * 65)
    for item in existing_artifacts:
        if item.is_dir():
            size = sum(f.stat().st_size for f in item.rglob("*") if f.is_file())
            print(f"  [DIR]  {item.name}  ({size:,} bytes)")
        else:
            size = item.stat().st_size
            print(f"  [FILE] {item.name}  ({size:,} bytes)")

    total_size = sum(
        f.stat().st_size
        for item in existing_artifacts
        for f in (item.rglob("*") if item.is_dir() else [item])
        if f.is_file()
    )

    print("-" * 65)
    rrprint(f"Total: [bold]{len(existing_artifacts)}[/bold] item(s), [bold]{total_size:,}[/bold] bytes")
    print()

    if not args.force:
        rrprint("[bright_green]DRY RUN: No files were deleted.")
        rrprint("Use --force or -f to actually delete the artifacts.")
        return 0

    # Actually delete
    print("Deleting artifacts...")
    errors = False

    for item in existing_artifacts:
        try:
            if item.is_dir():
                shutil.rmtree(item)
                rrprint(f"[bold bright_green]✓ Removed directory: {item.name}")
            else:
                item.unlink()
                rrprint(f"[bold bright_green]✓ Removed file: {item.name}")
        except Exception as e:
            rrprint(f"[bold bright_red]✗ Error removing {item.name}: {e}")
            errors = True

    print()
    if errors:
        rrprint(f"[bold bright_red]Some artifacts could not be deleted.")
        return 1
    else:
        print("Cleanup complete!")
        return 0


if __name__ == "__main__":
    sys.exit(main())
