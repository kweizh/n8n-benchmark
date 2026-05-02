import os
import pytest
import shutil

PROJECT_DIR = "/home/user/n8n-project"

def test_n8n_installed():
    assert shutil.which("n8n") is not None, "n8n is not installed"

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."
