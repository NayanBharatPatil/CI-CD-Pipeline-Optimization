def get_easy_config():
    return {
        "tasks": {
            "A": {"duration": 2, "cpu": 2},
            "B": {"duration": 2, "cpu": 1},
            "C": {"duration": 2, "cpu": 1},
        },
        "dependencies": {
            "B": ["A"],
            "C": ["A"]
        },
        "total_cpu": 4
    }


def grade(env):
    # simple scoring
    if all(t["status"] == "done" for t in env.tasks.values()):
        return 1.0
    return 0.0
