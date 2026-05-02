import os
import subprocess
import zipfile
import shutil
import pytest

PROJECT_DIR = "/home/user"
WORKFLOW_FILE = os.path.join(PROJECT_DIR, "workflow.json")
OUTPUT_ZIP = os.path.join(PROJECT_DIR, "output", "archive.zip")

def test_workflow_file_exists():
    assert os.path.isfile(WORKFLOW_FILE), f"Workflow file not found at {WORKFLOW_FILE}"

def test_workflow_execution():
    # Clean up output dir if it exists to ensure fresh execution
    output_dir = os.path.join(PROJECT_DIR, "output")
    if os.path.exists(OUTPUT_ZIP):
        os.remove(OUTPUT_ZIP)

    result = subprocess.run(
        ["n8n", "execute", "--file", WORKFLOW_FILE],
        capture_output=True,
        text=True,
        cwd=PROJECT_DIR
    )
    
    assert result.returncode == 0, f"Workflow execution failed. stderr: {result.stderr}\nstdout: {result.stdout}"

def test_zip_archive_created():
    assert os.path.isfile(OUTPUT_ZIP), f"Expected ZIP archive not found at {OUTPUT_ZIP}"

def test_zip_archive_contents():
    extract_dir = os.path.join(PROJECT_DIR, "extracted_output")
    os.makedirs(extract_dir, exist_ok=True)
    
    try:
        with zipfile.ZipFile(OUTPUT_ZIP, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
            
        file1_path = os.path.join(extract_dir, "file1.txt")
        file2_path = os.path.join(extract_dir, "file2.txt")
        
        assert os.path.isfile(file1_path), "file1.txt is missing from the ZIP archive."
        assert os.path.isfile(file2_path), "file2.txt is missing from the ZIP archive."
        
        with open(file1_path, 'r') as f1:
            content1 = f1.read().strip()
            assert content1 == "Content of file 1", f"Expected 'Content of file 1' in file1.txt, got '{content1}'"
            
        with open(file2_path, 'r') as f2:
            content2 = f2.read().strip()
            assert content2 == "Content of file 2", f"Expected 'Content of file 2' in file2.txt, got '{content2}'"
            
    finally:
        shutil.rmtree(extract_dir, ignore_errors=True)
