import os
import shutil
import pytest

def test_n8n_installed():
    assert shutil.which("n8n") is not None, "n8n is not installed in PATH"

def test_input_image_exists():
    assert os.path.isfile("/home/node/input.png"), "/home/node/input.png does not exist"
