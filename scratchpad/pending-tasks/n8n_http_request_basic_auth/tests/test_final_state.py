import os
import json
import pytest

PROJECT_DIR = "/home/user/n8n-project"
WORKFLOW_FILE = os.path.join(PROJECT_DIR, "workflow.json")
CREDENTIALS_FILE = os.path.join(PROJECT_DIR, "credentials.json")

def test_workflow_file_exists():
    assert os.path.isfile(WORKFLOW_FILE), f"workflow.json not found at {WORKFLOW_FILE}"

def test_workflow_http_request_node():
    with open(WORKFLOW_FILE) as f:
        try:
            workflow = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("workflow.json is not valid JSON")
            
    # Depending on how it's exported, it could be an array of nodes or an object with a "nodes" array
    nodes = []
    if isinstance(workflow, dict) and "nodes" in workflow:
        nodes = workflow["nodes"]
    elif isinstance(workflow, list):
        nodes = workflow
        
    http_nodes = [n for n in nodes if n.get("type") == "n8n-nodes-base.httpRequest"]
    assert len(http_nodes) == 1, f"Expected exactly one httpRequest node, found {len(http_nodes)}"
    
    node = http_nodes[0]
    params = node.get("parameters", {})
    
    assert params.get("url") == "https://httpbin.org/basic-auth/admin/secret", "URL is incorrect"
    assert params.get("method", "GET") == "GET", "Method is not GET"
    assert params.get("authentication") == "genericCredentialType", "Authentication type is not genericCredentialType"
    assert params.get("genericAuthType") == "httpBasicAuth", "Generic auth type is not httpBasicAuth"

def test_credentials_file_exists():
    assert os.path.isfile(CREDENTIALS_FILE), f"credentials.json not found at {CREDENTIALS_FILE}"

def test_credentials_content():
    with open(CREDENTIALS_FILE) as f:
        try:
            creds = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("credentials.json is not valid JSON")
            
    if not isinstance(creds, list):
        pytest.fail("credentials.json must contain a JSON array")
        
    basic_auth_creds = [c for c in creds if c.get("type") == "httpBasicAuth"]
    assert len(basic_auth_creds) >= 1, "No httpBasicAuth credential found"
    
    cred = basic_auth_creds[0]
    data = cred.get("data", {})
    
    assert data.get("user") == "admin" or data.get("username") == "admin", "Username is incorrect"
    assert data.get("password") == "secret", "Password is incorrect"
