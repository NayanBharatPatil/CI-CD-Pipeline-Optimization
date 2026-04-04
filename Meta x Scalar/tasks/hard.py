def get_hard_config():
    return {
        "tasks": {
            "A": {"duration": 3, "cpu": 2, "priority": 3},
            "B": {"duration": 2, "cpu": 2, "priority": 2},
            "C": {"duration": 2, "cpu": 1, "priority": 2},
            "D": {"duration": 3, "cpu": 2, "priority": 3},
            "E": {"duration": 1, "cpu": 1, "priority": 1},
        },
        "dependencies": {
            "B": ["A"],
            "C": ["A"],
            "D": ["B", "C"],
            "E": ["D"]
        }
    }