import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user"

def test_n8n_binary_available():
    assert shutil.which("n8n") is not None, "n8n binary not found in PATH."

def test_mock_api_server_script_exists():
    assert os.path.isfile(os.path.join(PROJECT_DIR, "server.py")), "Mock API server script server.py not found."
    
def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."