def get_easy_config():
    return {
        "tasks": {
            "A": {"duration": 2, "cpu": 2, "priority": 3},
            "B": {"duration": 1, "cpu": 1, "priority": 2},
        },
        "dependencies": {
            "B": ["A"]
        }
    }