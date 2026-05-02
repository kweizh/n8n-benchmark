import os
import subprocess
import time
import socket
import pytest
import json

PROJECT_DIR = "/home/user/n8n_project"
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
        time.sleep(5)
    return False

@pytest.fixture(scope="module")
def setup_n8n_and_slack():
    slack_token = os.environ["SLACK_TOKEN"]
    channel_name = f"n8n-alert-{get_channel_suffix()}"
    
    # Create Slack channel
    create_res = subprocess.run([
        "curl", "-sS", "-X", "POST",
        "-H", f"Authorization: Bearer {slack_token}",
        "-H", "Content-Type: application/json",
        "-d", json.dumps({"name": channel_name}),
        "https://slack.com/api/conversations.create"
    ], capture_output=True, text=True)
    
    create_data = json.loads(create_res.stdout)
    if not create_data.get("ok") and create_data.get("error") != "name_taken":
        pytest.fail(f"Failed to create Slack channel: {create_data}")

    if create_data.get("ok"):
        channel_id = create_data["channel"]["id"]
    else:
        # If name_taken, get the channel id
        list_res = subprocess.run([
            "curl", "-sS", "-H", f"Authorization: Bearer {slack_token}",
            "https://slack.com/api/conversations.list?limit=200&types=public_channel,private_channel"
        ], capture_output=True, text=True)
        list_data = json.loads(list_res.stdout)
        channels = list_data.get("channels", [])
        channel_id = next((c["id"] for c in channels if c["name"] == channel_name), None)
        if not channel_id:
            pytest.fail(f"Could not find existing channel {channel_name}")

    workflow_file = os.path.join(PROJECT_DIR, "workflow.json")
    if not os.path.isfile(workflow_file):
        pytest.fail(f"Workflow file {workflow_file} does not exist.")
        
    try:
        with open(workflow_file, "r") as f:
            workflow_data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail("Workflow file is not valid JSON.")

    if isinstance(workflow_data, dict):
        workflow_data["active"] = True
    elif isinstance(workflow_data, list) and len(workflow_data) > 0:
        workflow_data[0]["active"] = True
        
    with open(workflow_file, "w") as f:
        json.dump(workflow_data, f)
        
    import_result = subprocess.run(
        ["n8n", "import:workflow", f"--input={workflow_file}"],
        capture_output=True, text=True
    )
    if import_result.returncode != 0:
        pytest.fail(f"Failed to import workflow: {import_result.stderr}")

    env = os.environ.copy()
    env["N8N_PORT"] = "5678"
    process = subprocess.Popen(
        ["n8n", "start"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )

    if not wait_for_port(5678, timeout=120):
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("n8n failed to start on port 5678.")

    yield channel_id

    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)


def test_workflow_execution(setup_n8n_and_slack):
    channel_id = setup_n8n_and_slack
    slack_token = os.environ["SLACK_TOKEN"]
    
    # Trigger webhook
    trigger_res = subprocess.run([
        "curl", "-sS", "-X", "POST",
        "-H", "Content-Type: application/json",
        "-d", '{"message": "System overload"}',
        "http://localhost:5678/webhook/slack-alert"
    ], capture_output=True, text=True)
    
    # Wait a moment for n8n to process and send to Slack
    time.sleep(5)
    
    # Verify Slack message
    history_res = subprocess.run([
        "curl", "-sS", "-X", "GET",
        "-H", f"Authorization: Bearer {slack_token}",
        f"https://slack.com/api/conversations.history?channel={channel_id}&limit=10"
    ], capture_output=True, text=True)
    
    assert history_res.returncode == 0, f"Failed to get Slack history: {history_res.stderr}"
    history_data = json.loads(history_res.stdout)
    assert history_data.get("ok"), f"Slack API error: {history_data}"
    
    messages = history_data.get("messages", [])
    message_texts = [m.get("text", "") for m in messages]
    
    expected_msg = "Alert: System overload"
    assert any(expected_msg in text for text in message_texts), \
        f"Expected message '{expected_msg}' not found in channel. Found: {message_texts}"