import importlib.util
from pathlib import Path
from types import SimpleNamespace

import pytest

utils_path = Path(__file__).resolve().parents[1] / "scripts" / "utils.py"
spec = importlib.util.spec_from_file_location("scripts_utils", utils_path)
utils = importlib.util.module_from_spec(spec)
spec.loader.exec_module(utils)


@pytest.fixture(autouse=True)
def silence_console_output(monkeypatch):
    """Prevent rich console output during tests."""
    monkeypatch.setattr(utils, "rrprint", lambda *args, **kwargs: None)


def test_colour_filename():
    assert utils.colour_filename("example.txt") == "[bold bright_magenta]example.txt[/bold bright_magenta]"


def test_run_command_success(monkeypatch):
    monkeypatch.setattr(utils.subprocess, "run", lambda cmd: SimpleNamespace(returncode=0))
    assert utils.run_command(["echo", "hello"], "Test command") is True


def test_run_command_failure(monkeypatch):
    monkeypatch.setattr(utils.subprocess, "run", lambda cmd: SimpleNamespace(returncode=5))
    assert utils.run_command(["false"], "Failing command") is False


def test_move_file_creates_parent_and_moves(tmp_path):
    src = tmp_path / "source.txt"
    src.write_text("hello")
    dest = tmp_path / "nested" / "dest.txt"

    assert utils.move_file(src, dest, "Move file") is True
    assert dest.exists()
    assert not src.exists()


def test_move_file_missing_source(tmp_path):
    missing = tmp_path / "does_not_exist.txt"
    dest = tmp_path / "dest.txt"

    assert utils.move_file(missing, dest) is False
    assert not dest.exists()


def test_copy_file(tmp_path):
    src = tmp_path / "source.txt"
    src.write_text("copy content")
    dest = tmp_path / "copied" / "dest.txt"
    dest.parent.mkdir(parents=True)

    assert utils.copy_file(src, dest, "Copy file") is True
    assert dest.exists()
    assert dest.read_text() == "copy content"
    assert src.exists()


def test_unlink_file_and_directory(tmp_path):
    file_path = tmp_path / "file.txt"
    file_path.write_text("delete me")
    dir_path = tmp_path / "emptydir"
    dir_path.mkdir()

    assert utils.unlink_file(file_path) is True
    assert not file_path.exists()
    assert utils.unlink_directory(dir_path) is True
    assert not dir_path.exists()


def test_remove_path_file_and_directory(tmp_path):
    file_path = tmp_path / "file.txt"
    file_path.write_text("delete me")
    dir_path = tmp_path / "nested_dir"
    dir_path.mkdir()
    (dir_path / "child.txt").write_text("child")

    assert utils.remove_path(file_path) is True
    assert not file_path.exists()

    assert utils.remove_path(dir_path) is True
    assert not dir_path.exists()


def test_remove_files_and_directories_alias(tmp_path):
    file_path = tmp_path / "file.txt"
    file_path.write_text("content")
    dir_path = tmp_path / "dir"
    dir_path.mkdir()

    assert utils.remove_files_and_directories([file_path, dir_path]) is True
    assert not file_path.exists()
    assert not dir_path.exists()
    assert utils.remove_artifacts is utils.remove_files_and_directories


def test_create_zip_missing_source(tmp_path):
    output_file = tmp_path / "archive.zip"
    assert utils.create_zip(tmp_path / "nonexistent_dir", output_file) is False


def test_create_zip_success(monkeypatch, tmp_path):
    source_dir = tmp_path / "source_dir"
    source_dir.mkdir()
    (source_dir / "file.txt").write_text("archive content")

    output_file = tmp_path / "archive.zip"
    monkeypatch.setattr(utils.subprocess, "run", lambda cmd: SimpleNamespace(returncode=0))

    assert utils.create_zip(source_dir, output_file) is True
    assert output_file.parent.exists()
