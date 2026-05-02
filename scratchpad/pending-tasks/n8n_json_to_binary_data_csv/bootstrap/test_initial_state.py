import os
import shutil

def test_n8n_binary_available():
    assert shutil.which("n8n") is not None, "n8n binary not found in PATH."

def test_home_node_directory_exists():
    assert os.path.isdir("/home/node"), "/home/node directory does not exist."
