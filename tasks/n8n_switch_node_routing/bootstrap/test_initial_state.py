import os
import shutil
import pytest

def test_n8n_binary_available():
    assert shutil.which("n8n") is not None, "n8n binary not found in PATH."

def test_home_user_exists():
    assert os.path.isdir("/home/user"), "/home/user directory does not exist."
