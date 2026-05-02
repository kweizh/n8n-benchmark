import os

def test_initial_state():
    project_dir = "/home/user/myproject"
    data_file = os.path.join(project_dir, "data.csv")
    
    assert os.path.isdir(project_dir), f"Project directory {project_dir} does not exist"
    assert os.path.isfile(data_file), f"Data file {data_file} does not exist"
