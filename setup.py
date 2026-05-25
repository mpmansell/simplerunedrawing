"""Setup script for SimpleRuneDrawing package."""

from setuptools import setup, find_packages

setup(
    name="simplerunedrawing",
    version="0.1.0",
    description="A Simple Rune Drawing application",
    long_description=open("readme.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    author="Mark Peter Mansell",
    author_email="mark.mansell@gmail.com",
    url="https://github.com/yourusername/simplerunedrawing",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.13",
    install_requires=[
        "pillow>=12.2.0,<13.0.0",
        "typer>=0.25.1,<0.26.0",
    ],

    entry_points={
        "console_scripts": [
            "drawrunes=__main__:app",
            "simplerunedrawing=__main__:app",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.13",
    ],
)
