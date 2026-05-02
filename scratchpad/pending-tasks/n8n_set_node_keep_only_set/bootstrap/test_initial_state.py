import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/workspace"

def test_n8n_binary_available():
    assert shutil.which("n8n") is not None, "n8n binary not found in PATH."

def test_workspace_directory_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."
