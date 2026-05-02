import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/n8n-task"

def test_n8n_binary_available():
    assert shutil.which("n8n") is not None, "n8n binary not found in PATH."

def test_psql_binary_available():
    assert shutil.which("psql") is not None, "psql binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_start_script_exists():
    start_script = os.path.join(PROJECT_DIR, "start.sh")
    assert os.path.isfile(start_script), f"Start script {start_script} does not exist."
