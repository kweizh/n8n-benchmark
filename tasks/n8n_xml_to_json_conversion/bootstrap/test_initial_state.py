import os
import shutil
import pytest

def test_n8n_binary_available():
    assert shutil.which("n8n") is not None, "n8n binary not found in PATH."

def test_working_directory_exists():
    assert os.path.isdir("/home/user"), "Working directory /home/user does not exist."

def test_workflow_file_does_not_exist():
    assert not os.path.exists("/home/user/workflow.json"), "workflow.json should not exist initially."