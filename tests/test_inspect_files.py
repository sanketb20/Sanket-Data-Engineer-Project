from pathlib import Path

from inspect_files import inspect_files


def test_inspect_files_returns_file_names(tmp_path):

    (tmp_path / "file1.csv").write_text("data")
    (tmp_path / "file2.json").write_text("data")

    result = inspect_files(tmp_path)

    assert "file1.csv" in result
    assert "file2.json" in result
    assert len(result) == 2


def test_inspect_files_ignores_directories(tmp_path):

    (tmp_path / "file1.csv").write_text("data")
    (tmp_path / "test_folder").mkdir()

    result = inspect_files(tmp_path)

    assert result == ["file1.csv"]
    assert "test_folder" not in result
    