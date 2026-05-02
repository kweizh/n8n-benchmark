import json
import os

def test_workflow_exists():
    assert os.path.exists("/home/user/workflow.json"), "workflow.json should exist"

def test_workflow_content():
    with open("/home/user/workflow.json", "r") as f:
        data = json.load(f)
        nodes = data.get("nodes", [])
        node_names = [n.get("name") for n in nodes]
        assert "Mock HTML" in node_names, "Mock HTML node should exist initially"
        assert "HTML Extract" not in node_names, "HTML Extract node should not exist initially"