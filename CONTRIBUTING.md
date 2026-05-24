# Contributing

Contributions are welcome, and they are greatly appreciated! Every little bit helps, and credit will always be given.

You can contribute in many ways:

## Types of Contributions

### Report Bugs

Report bugs at https://github.com/mpmansell/simplerunedrawing/issues.

If you are reporting a bug, please include:

- Your operating system name and version.
- Any details about your local setup that might be helpful in troubleshooting.
- Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help wanted" is open to whoever wants to implement it.

### Implement Features

Look through the GitHub issues for features. Anything tagged with "enhancement" and "help wanted" is open to whoever wants to implement it.

### Write Documentation

SimpleRuneDrawing could always use more documentation, whether as part of the official docs, in docstrings, or even on the web in blog posts, articles, and such.

### Submit Feedback

The best way to send feedback is to file an issue at https://github.com/mpmansell/simplerunedrawing/issues.

If you are proposing a feature:

- Explain in detail how it would work.
- Keep the scope as narrow as possible, to make it easier to implement.
- Remember that this is a volunteer-driven project, and that contributions are welcome :)

## Prerequisites

The following tools will need to be installed

### Required

- git - [Git Git https://git-scm.com](https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://git-scm.com/&ved=2ahUKEwjpuNPwlNKRAxVaQ_EDHRPtOxUQFnoECA8QAQ&usg=AOvVaw1lFNWgbWf8FsbaoU4AOPBr)
- GNU Make - [Make - GNU Project - Free Software Foundation GNU https://www.gnu.org › software › make](https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://www.gnu.org/software/make/&ved=2ahUKEwi8u5HclNKRAxXvRPEDHZWNCo4QFnoECCUQAQ&usg=AOvVaw1zM-Js4YqRdqmHDbyhZJQE)
- Python poetry - [Poetry - Python dependency management and packaging ... Poetry - Python https://python-poetry.org](https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://python-poetry.org/&ved=2ahUKEwjmh93PlNKRAxXbR_EDHU_1FU8QFnoECBoQAQ&usg=AOvVaw3Jp8q7OO7XkcY8Tq4tDe30)
- Visual Studio Code - [Visual Studio Code - The open source AI code editor Visual Studio Code https://code.visualstudio.com](https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://code.visualstudio.com/&ved=2ahUKEwiuraOMldKRAxWABdsEHZGiIVQQFnoECA0QAQ&usg=AOvVaw15O90sm1ios8AUpw56hCml) or your editor of choice (Makefile will need modifying to suit)

**Note**: Use `make vsc`, or `poetry run code -n .` to start Visual Studio Code as this will ensure that Intellicode, or the AI language server, will be aware of the imported modules (If, for instance, `numpy` objects are not appropriately highlighted, or typed, you might have started Vsc outside of the poetry manage virtual environment.)

### Optional

These are optional and depend on whether, or not, you need [Docker](https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://en.wikipedia.org/wiki/Docker_(software)&ved=2ahUKEwia-fTvldKRAxWGRPEDHe1NGxEQFnoECA0QAQ&usg=AOvVaw0z0Prdwu6k0Lwh1-puSNOO) or to generate some extended documentation (NOTE: Makefile incomplete for documentation)

- [Docker: Accelerated Container Application Development](https://www.docker.com/)
- [a2ps - GNU Project - Free Software Foundation (FSF) GNU https://www.gnu.org › software › a2ps](https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://www.gnu.org/software/a2ps/&ved=2ahUKEwjcgf-bltKRAxWJRPEDHWkqGmYQFnoECAwQAQ&usg=AOvVaw3P6iN1t8AMBULVbGHgdhI5)
- [simaranjit/ps2pdf: Batch PS to PDF file converter. GitHub https://github.com › simaranjit › ps2pdf](https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://github.com/simaranjit/ps2pdf&ved=2ahUKEwiXiIulltKRAxUVVfEDHXqtLXcQFnoECB4QAQ&usg=AOvVaw1o105HDJH2A5JcT5OJvmes)
- Doxygen - [Doxygen homepage Doxygen https://www.doxygen.nl](https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://www.doxygen.nl/&ved=2ahUKEwiVs97XltKRAxUvQ_EDHQ6TLE4QFnoECCIQAQ&usg=AOvVaw0g-2LaEwos-xH3xaX9Jq0-)

**Note**: run `make help` to get a list of predefined Make targets for this project.

## Get Started

Ready to contribute? Here's how to set up `simplerunedrawing` for local development.

1. Fork the `simplerunedrawing` repo on GitHub.
2. Clone your fork locally:

   ```sh
   git clone git@github.com:your_name_here/simplerunedrawing.git
   ```

3. Create the Poetry managed virtual environment

   ```sh
   cd simplerunedrawing/
   poetry install
   ```

4. Create a branch for local development:

   ```sh
   git checkout -b name-of-your-bugfix-or-feature
   ```

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass linting and the tests

   ```sh
   make lint
   make test
   # Or
   make test-all
   ```

   The linting and test tools are declared in the `pyproject.toml` file and any changes in requirements should be reflected here.

6. Commit your changes and push your branch to GitHub:

   ```sh
   git add .
   git commit -m "Your detailed description of your changes."
   git push origin name-of-your-bugfix-or-feature
   ```

7. Submit a pull request through the GitHub website.

## Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put your new functionality into a function with a docstring, and add the feature to the list in README.md.
3. The pull request should work for Python 3.14. Tests run in GitHub Actions on every pull request to the main branch, make sure that the tests pass for all supported Python versions.

## Tips

To run a subset of tests:

```sh
pytest tests.test_simplerunedrawing
```

## Deploying

A reminder for the maintainers on how to deploy. Make sure all your changes are committed (including an entry in HISTORY.md). Then run:

```sh
bump2version patch # possible: major / minor / patch
git push
git push --tags
```

You can set up a [GitHub Actions workflow](https://docs.github.com/en/actions/use-cases-and-examples/building-and-testing/building-and-testing-python#publishing-to-pypi) to automatically deploy your package to PyPI when you push a new tag.

## Code of Conduct

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.
