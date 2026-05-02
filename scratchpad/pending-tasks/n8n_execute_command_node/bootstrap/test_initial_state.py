import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/node"

def test_n8n_binary_available():
    assert shutil.which("n8n") is not None, "n8n binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_script_exists_and_executable():
    script_path = os.path.join(PROJECT_DIR, "script.sh")
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_script_output():
    script_path = os.path.join(PROJECT_DIR, "script.sh")
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert '{"id": 42, "status": "completed"}' in result.stdout, "Script does not output the expected JSON."
