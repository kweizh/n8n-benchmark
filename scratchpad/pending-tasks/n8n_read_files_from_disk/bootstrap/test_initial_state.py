import os
import shutil
import pytest

PROJECT_DIR = "/home/user"
DATA_DIR = "/home/user/data"

def test_n8n_binary_available():
    assert shutil.which("n8n") is not None, "n8n binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_data_dir_exists():
    assert os.path.isdir(DATA_DIR), f"Data directory {DATA_DIR} does not exist."

def test_data_files_exist():
    files = ["report.csv", "summary.txt", "logo.png"]
    for file in files:
        file_path = os.path.join(DATA_DIR, file)
        assert os.path.isfile(file_path), f"File {file_path} does not exist."
