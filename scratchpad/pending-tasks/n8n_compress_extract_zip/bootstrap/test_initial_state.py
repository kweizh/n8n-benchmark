import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user"

def test_n8n_binary_available():
    assert shutil.which("n8n") is not None, "n8n binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_files_exist():
    file1 = os.path.join(PROJECT_DIR, "file1.txt")
    file2 = os.path.join(PROJECT_DIR, "file2.txt")
    assert os.path.isfile(file1), f"File {file1} does not exist."
    assert os.path.isfile(file2), f"File {file2} does not exist."

def test_output_dir_exists():
    output_dir = os.path.join(PROJECT_DIR, "output")
    assert os.path.isdir(output_dir), f"Output directory {output_dir} does not exist."
