import os
import shutil
import subprocess

PROJECT_DIR = "/home/user/n8n_project"
TRIAL_ID_FILE = "/logs/artifacts/trial_id"

def test_n8n_installed():
    assert shutil.which("n8n") is not None, "n8n binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_trial_id_file_exists():
    assert os.path.isfile(TRIAL_ID_FILE), f"Trial ID file {TRIAL_ID_FILE} does not exist."

def test_slack_token_in_env():
    assert "SLACK_TOKEN" in os.environ, "SLACK_TOKEN environment variable is not set."
