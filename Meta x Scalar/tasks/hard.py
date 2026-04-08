def get_hard_config():
    return {
        "tasks": {
            "A": {"duration": 4, "cpu": 2},
            "B": {"duration": 3, "cpu": 1},
            "C": {"duration": 3, "cpu": 1},
            "D": {"duration": 2, "cpu": 2},
            "E": {"duration": 1, "cpu": 1},
        },
        "dependencies": {
            "B": ["A"],
            "C": ["A"],
            "D": ["B", "C"],
            "E": ["D"]
        },
        "total_cpu": 4
    }


def grade(env):
    
    if env.time == 0:
        return 0.0

    completed = sum(1 for t in env.tasks.values() if t["status"] == "done")
    efficiency = completed / len(env.tasks)

    return min(1.0, efficiency)
