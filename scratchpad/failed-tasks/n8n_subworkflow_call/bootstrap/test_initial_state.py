import os
import shutil

def test_n8n_binary_available():
    assert shutil.which("n8n") is not None, "n8n binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir("/home/user/n8n_project"), "/home/user/n8n_project directory does not exist."
