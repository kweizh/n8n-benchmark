import os
import shutil
import pytest
import subprocess

PROJECT_DIR = "/home/user/workspace"

def test_n8n_binary_available():
    assert shutil.which("n8n") is not None, "n8n binary not found in PATH."

def test_workspace_exists():
    assert os.path.isdir(PROJECT_DIR), f"Workspace directory {PROJECT_DIR} does not exist."

def test_input_file_exists():
    input_path = os.path.join(PROJECT_DIR, "input.txt")
    assert os.path.isfile(input_path), f"Input file {input_path} does not exist."
    with open(input_path, "r") as f:
        content = f.read()
    assert content.strip() == "Hello, n8n world!", f"Expected 'Hello, n8n world!' in input.txt, got: {content}"

def test_workflow_file_exists():
    workflow_path = os.path.join(PROJECT_DIR, "workflow.json")
    assert os.path.isfile(workflow_path), f"Workflow file {workflow_path} does not exist."
    with open(workflow_path, "r") as f:
        content = f.read()
    assert "n8n-nodes-base.readWriteFile" in content, "Expected readWriteFile node in workflow.json."
