import os
import subprocess
import json
import time
import socket
import pytest

PROJECT_DIR = "/home/user/workspace"
WORKFLOW_FILE = os.path.join(PROJECT_DIR, "error_workflow.json")
TRIAL_ID_FILE = "/logs/artifacts/trial_id"

def get_trial_id():
    with open(TRIAL_ID_FILE, "r") as f:
        return f.read().strip()

def get_channel_suffix():
    return get_trial_id().lower()

def wait_for_port(port, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                return True
        time.sleep(2)
    return False

@pytest.fixture(scope="module")
def setup_n8n():
    assert os.path.isfile(WORKFLOW_FILE), f"Workflow file {WORKFLOW_FILE} does not exist."
    
    # 0. Create Slack channel
    channel_suffix = get_channel_suffix()
    channel_name = f"error-alerts-{channel_suffix}"
    slack_token = os.environ["SLACK_TOKEN"]
    
    # Try to create channel
    subprocess.run([
        "curl", "-sS", "-X", "POST",
        "-H", f"Authorization: Bearer {slack_token}",
        "-H", "Content-Type: application/json",
        "-d", json.dumps({"name": channel_name}),
        "https://slack.com/api/conversations.create"
    ], capture_output=True)
    
    # 1. Prepare credentials
    creds = [{
        "name": "Slack Bot",
        "type": "slackApi",
        "data": {
            "accessToken": os.environ["SLACK_TOKEN"]
        }
    }]
    with open("/tmp/creds.json", "w") as f:
        json.dump(creds, f)
        
    subprocess.run(["n8n", "import:credentials", "--input=/tmp/creds.json"], check=True)
    
    # 2. Prepare user workflow
    with open(WORKFLOW_FILE, "r") as f:
        user_wf = json.load(f)
    
    user_wf["id"] = "999"
    user_wf["active"] = True
    
    with open("/tmp/error_workflow.json", "w") as f:
        json.dump(user_wf, f)
        
    subprocess.run(["n8n", "import:workflow", "--input=/tmp/error_workflow.json"], check=True)
    
    # 3. Prepare failing workflow
    failing_wf = {
      "id": "1000",
      "name": "Failing Workflow",
      "active": True,
      "nodes": [
        {
          "parameters": {
            "path": "fail-test",
            "options": {}
          },
          "name": "Webhook",
          "type": "n8n-nodes-base.webhook",
          "typeVersion": 1,
          "position": [250, 300],
          "webhookId": "test-webhook-id"
        },
        {
          "parameters": {
            "jsCode": "throw new Error('Test error');"
          },
          "name": "Code",
          "type": "n8n-nodes-base.code",
          "typeVersion": 1,
          "position": [450, 300]
        }
      ],
      "connections": {
        "Webhook": {
          "main": [
            [
              {
                "node": "Code",
                "type": "main",
                "index": 0
              }
            ]
          ]
        }
      },
      "settings": {
        "errorWorkflow": "999"
      }
    }
    with open("/tmp/failing_workflow.json", "w") as f:
        json.dump(failing_wf, f)
        
    subprocess.run(["n8n", "import:workflow", "--input=/tmp/failing_workflow.json"], check=True)
    
    # 4. Start n8n
    env = os.environ.copy()
    env["WEBHOOK_URL"] = "http://localhost:5678/"
    process = subprocess.Popen(
        ["n8n", "start"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )
    
    if not wait_for_port(5678):
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("n8n failed to start.")
        
    # Wait an extra 5 seconds for workflows to activate
    time.sleep(5)
        
    # 5. Trigger failing workflow via webhook
    # We use subprocess to curl the webhook
    result = subprocess.run(["curl", "-s", "-X", "POST", "http://localhost:5678/webhook/fail-test"], capture_output=True, text=True)
    
    # Wait for error workflow to execute and send Slack message
    time.sleep(10)
    
    yield
    
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=10)

def test_slack_message_sent(setup_n8n):
    channel_suffix = get_channel_suffix()
    expected_channel = f"error-alerts-{channel_suffix}"
    slack_token = os.environ["SLACK_TOKEN"]
    
    # Get list of channels to find the ID of our target channel
    result = subprocess.run([
        "curl", "-sS", "-H", f"Authorization: Bearer {slack_token}",
        "https://slack.com/api/conversations.list?limit=200&types=public_channel,private_channel"
    ], capture_output=True, text=True)
    
    assert result.returncode == 0, f"curl conversations.list failed: {result.stderr}"
    data = json.loads(result.stdout)
    assert data.get("ok"), f"Slack API error: {data}"
    
    channel_id = None
    for c in data.get("channels", []):
        if c["name"] == expected_channel:
            channel_id = c["id"]
            break
            
    assert channel_id is not None, f"Channel {expected_channel} not found in Slack."
    
    # Get messages from the channel
    result = subprocess.run([
        "curl", "-sS", "-H", f"Authorization: Bearer {slack_token}",
        f"https://slack.com/api/conversations.history?channel={channel_id}&limit=10"
    ], capture_output=True, text=True)
    
    assert result.returncode == 0, f"curl conversations.history failed: {result.stderr}"
    data = json.loads(result.stdout)
    assert data.get("ok"), f"Slack API error: {data}"
    
    messages = data.get("messages", [])
    found_message = False
    for msg in messages:
        text = msg.get("text", "")
        if "Error in execution" in text:
            found_message = True
            break
            
    assert found_message, f"Did not find expected error message in channel {expected_channel}. Messages found: {[m.get('text') for m in messages]}"
