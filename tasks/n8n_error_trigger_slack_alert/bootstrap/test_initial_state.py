import os
import shutil
import pytest

PROJECT_DIR = "/home/user/workspace"
TRIAL_ID_FILE = "/logs/artifacts/trial_id"

def test_n8n_binary_available():
    assert shutil.which("n8n") is not None, "n8n binary not found in PATH."

def test_workspace_directory_exists():
    assert os.path.isdir(PROJECT_DIR), f"Workspace directory {PROJECT_DIR} does not exist."

def test_slack_token_env_var_exists():
    assert "SLACK_TOKEN" in os.environ, "SLACK_TOKEN environment variable is missing."

def test_trial_id_file_exists():
    assert os.path.isfile(TRIAL_ID_FILE), f"Trial ID file {TRIAL_ID_FILE} not found."
