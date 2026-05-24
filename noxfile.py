import nox
import os

# --------------------------------------------------------------------------------
# Default notebook
# --------------------------------------------------------------------------------
DEFAULT_NOTEBOOK = "notebooks/notebook1.ipynb"

# --------------------------------------------------------------------------------
# Utility functions
# --------------------------------------------------------------------------------
def run_poetry(session, *args):
    """Run a Poetry command in an external shell."""
    session.run("poetry", *args, external=True)


# --------------------------------------------------------------------------------
# Nox sessions
# --------------------------------------------------------------------------------

@nox.session
def install(session):
    """Install dependencies with Poetry."""
    run_poetry(session, "install")


@nox.session
def poetry_install(session):
    """Alias for 'install'."""
    session.notify("install")


@nox.session
def poetry_update(session):
    """Update dependencies with Poetry."""
    run_poetry(session, "update")


@nox.session
def show_env(session):
    """Show the Python path of the Poetry virtual environment."""
    run_poetry(session, "env", "info", "--path")


@nox.session
def venv_activate(session):
    """Instructions to activate the Poetry virtual environment."""
    print("\nRun the following commands to activate the Poetry virtual environment:\n")
    print("PowerShell:")
    print("    Invoke-Expression (poetry env activate)")
    print("Bash (Linux/macOS):")
    print("    source `poetry env info --path`/bin/activate")
    print("Git Bash:")
    print("    source `cygpath -u $$(poetry env info --path)/Scripts/activate`\n")
    print("Then run `which python` or `nox -s show_env` to verify the python executable.\n")


@nox.session
def run_notebook(session):
    """
    Open a notebook in Visual Studio Code.

    Usage:
      nox -s run_notebook -- notebooks/notebook2.ipynb
      (defaults to notebooks/notebook1.ipynb if no argument is provided)
    """
    notebook = session.posargs[0] if session.posargs else DEFAULT_NOTEBOOK
    session.run("poetry", "run", "code", "-n", ".", notebook, external=True)


@nox.session
def vsc(session):
    """Open the project in Visual Studio Code."""
    session.run("poetry", "run", "code", "-n", ".", external=True)


@nox.session
def git_init(session):
    """Initialize a new git repository."""
    session.run("git", "init", external=True)
    session.run("git", "add", ".", external=True)
    session.run("git", "commit", "-m", "Initial commit", external=True)


@nox.session
def requirements(session):
    """Export dependencies to requirements.txt."""
    run_poetry(session, "self", "add", "poetry-plugin-export@latest")
    run_poetry(session, "export", "-f", "requirements.txt", "--output", "requirements.txt", "--without-hashes")


# --------------------------------------------------------------------------------
# Help session
# --------------------------------------------------------------------------------

@nox.session
def help(session):
    """
    Show a color-coded help message with all available Nox sessions.
    """
    # ANSI color codes
    COLOR_RESET = "\033[0m"
    COLOR_PYTHON = "\033[94m"  # Blue
    COLOR_POETRY = "\033[92m"  # Green
    COLOR_GIT = "\033[93m"     # Yellow
    COLOR_OTHER = "\033[95m"   # Magenta

    print("\nAvailable Nox sessions:\n")

    for name, func in globals().items():
        if callable(func) and hasattr(func, "__module__") and func.__module__ == __name__:
            doc = func.__doc__.strip() if func.__doc__ else ""

            # Color-code by type
            if "poetry" in name or name in ["install", "requirements"]:
                color = COLOR_POETRY
            elif "git" in name:
                color = COLOR_GIT
            elif name in ["run_notebook", "vsc", "venv_activate", "show_env"]:
                color = COLOR_PYTHON
            else:
                color = COLOR_OTHER

            print(f"{color}{name:<25}{COLOR_RESET}  {doc}")

    print("\nRun a session with: nox -s <session_name> [optional arguments]\n")
