import os
import subprocess
import pytest
import time
import socket

PROJECT_DIR = "/home/user"
WORKFLOW_FILE = os.path.join(PROJECT_DIR, "workflow.json")
TOTAL_FILE = os.path.join(PROJECT_DIR, "total.txt")

def wait_for_port(port, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                return True
        time.sleep(0.5)
    return False

@pytest.fixture(scope="module", autouse=True)
def start_mock_api():
    # Start the mock API server if it's not already running
    if not wait_for_port(3000, timeout=1):
        process = subprocess.Popen(
            ["python3", "/home/user/server.py"],
            cwd=PROJECT_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=os.setsid
        )
        if not wait_for_port(3000):
            import signal
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            pytest.fail("Mock API failed to start on port 3000.")
        yield
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        process.wait(timeout=5)
    else:
        yield

def test_workflow_execution():
    """Priority 1: Use n8n CLI to execute the workflow and verify it succeeds."""
    assert os.path.isfile(WORKFLOW_FILE), f"Workflow file not found at {WORKFLOW_FILE}"
    
    # Execute the workflow
    result = subprocess.run(
        ["n8n", "execute", "--file=" + WORKFLOW_FILE],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    
    assert result.returncode == 0, f"'n8n execute' failed: {result.stderr}\nStdout: {result.stdout}"
    
def test_total_users_file():
    """Priority 3 fallback: check the total.txt file."""
    assert os.path.isfile(TOTAL_FILE), f"{TOTAL_FILE} was not created by the workflow."
    
    with open(TOTAL_FILE, "r") as f:
        content = f.read().strip()
        
    assert content == "5", f"Expected total.txt to contain '5', but got '{content}'"