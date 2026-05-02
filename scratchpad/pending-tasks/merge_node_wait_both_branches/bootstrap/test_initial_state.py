import os
import subprocess

def test_initial_state():
    # Verify workspace directory exists
    assert os.path.exists("/home/user/workspace"), "Workspace directory does not exist"
    
    # Verify n8n is installed globally
    result = subprocess.run(["n8n", "--version"], capture_output=True, text=True)
    assert result.returncode == 0, f"n8n is not installed or not working: {result.stderr}"
