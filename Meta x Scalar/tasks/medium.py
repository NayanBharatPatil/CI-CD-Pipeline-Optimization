def get_medium_config():
    return {
        "tasks": {
            "A": {"duration": 3, "cpu": 2},
            "B": {"duration": 2, "cpu": 1},
            "C": {"duration": 2, "cpu": 1},
            "D": {"duration": 1, "cpu": 1},
        },
        "dependencies": {
            "B": ["A"],
            "C": ["A"],
            "D": ["B", "C"]
        },
        "total_cpu": 4
    }


def grade(env):
    completed = sum(1 for t in env.tasks.values() if t["status"] == "done")
    total = len(env.tasks)
    return completed / total
