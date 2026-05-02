import os
import subprocess
import json
import pytest
import time

PROJECT_DIR = "/home/user/n8n-task"

@pytest.fixture(scope="module", autouse=True)
def setup_environment():
    # Make sure n8n is running since we need it for CLI export if it talks to the DB
    # The setup script should have been executed by the verifier, but just in case
    # we export using the CLI directly.
    pass

def test_workflow_exported_and_exists():
    """Priority 1: Use n8n CLI to export workflows and verify."""
    result = subprocess.run(
        ["n8n", "export:workflow", "--all", "--output=/tmp/workflows.json"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"'n8n export:workflow' failed: {result.stderr}"
    assert os.path.isfile("/tmp/workflows.json"), "Expected /tmp/workflows.json to be created."

    with open("/tmp/workflows.json") as f:
        workflows = json.load(f)

    # Workflows export format is typically an array or an object with a workflows array
    # Let's handle both
    if isinstance(workflows, dict) and "workflows" in workflows:
        workflows_list = workflows["workflows"]
    elif isinstance(workflows, list):
        workflows_list = workflows
    else:
        pytest.fail(f"Unexpected workflows.json format: {type(workflows)}")

    db_cleanup_wf = next((w for w in workflows_list if w.get("name") == "Database Cleanup Workflow"), None)
    assert db_cleanup_wf is not None, "Workflow 'Database Cleanup Workflow' not found."

    # Verify it is active
    assert db_cleanup_wf.get("active") is True, "The workflow is not active."

    nodes = db_cleanup_wf.get("nodes", [])

    # Check for Schedule Trigger node
    schedule_node = next((n for n in nodes if n.get("type") == "n8n-nodes-base.scheduleTrigger"), None)
    assert schedule_node is not None, "No Schedule Trigger node found in the workflow."
    
    # The rule is inside parameters.rule
    params = schedule_node.get("parameters", {})
    # It might be nested in rule.value or just rule depending on versions
    # Let's check the JSON dump
    rule_found = False
    if "rule" in params:
        rule_val = params["rule"]
        if isinstance(rule_val, dict) and rule_val.get("value") == "0 3 * * *":
            rule_found = True
        elif rule_val == "0 3 * * *":
            rule_found = True
    assert rule_found, f"Schedule Trigger node does not have the expected cron rule '0 3 * * *'. Found parameters: {params}"

    # Check for Postgres node
    postgres_node = next((n for n in nodes if n.get("type") == "n8n-nodes-base.postgres"), None)
    assert postgres_node is not None, "No Postgres node found in the workflow."
    
    pg_params = postgres_node.get("parameters", {})
    operation = pg_params.get("operation")
    assert operation == "executeQuery", f"Postgres node operation is not 'executeQuery', found: {operation}"
    
    query = pg_params.get("query")
    expected_query = "DELETE FROM logs WHERE created_at < NOW() - INTERVAL '30 days';"
    assert query == expected_query, f"Postgres node query is incorrect. Expected: {expected_query}, Found: {query}"


def test_credentials_exported_and_exists():
    """Priority 1: Use n8n CLI to export credentials and verify."""
    result = subprocess.run(
        ["n8n", "export:credentials", "--all", "--output=/tmp/credentials.json"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"'n8n export:credentials' failed: {result.stderr}"
    assert os.path.isfile("/tmp/credentials.json"), "Expected /tmp/credentials.json to be created."

    with open("/tmp/credentials.json") as f:
        credentials = json.load(f)

    if isinstance(credentials, dict) and "credentials" in credentials:
        creds_list = credentials["credentials"]
    elif isinstance(credentials, list):
        creds_list = credentials
    else:
        pytest.fail(f"Unexpected credentials.json format: {type(credentials)}")

    pg_cred = next((c for c in creds_list if c.get("name") == "postgres_creds"), None)
    assert pg_cred is not None, "Credential 'postgres_creds' not found."
    
    cred_type = pg_cred.get("type")
    assert cred_type == "postgres", f"Credential type is not 'postgres', found: {cred_type}"
