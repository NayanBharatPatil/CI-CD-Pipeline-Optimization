class PipelineEnv:
    def __init__(self):
        self.tasks = {}
        self.dependencies = {}
        self.current_time = 0
        self.done = False

        self.total_cpu = 4
        self.used_cpu = 0

   def reset(self, config=None):
    if config is None:
        raise ValueError("Config must be provided")

    self.tasks = {
        k: {
            "status": "pending",
            "duration": v["duration"],
            "cpu": v["cpu"]
        }
        for k, v in config["tasks"].items()
    }

    self.dependencies = config.get("dependencies", {})
    self.total_cpu = config.get("total_cpu", 4)
    self.used_cpu = 0
    self.time = 0

    return self.state()

    def state(self):
        return {
            "tasks": self.tasks,
            "time": self.current_time,
            "cpu": {
                "total": self.total_cpu,
                "used": self.used_cpu
            }
        }

    def step(self, action):

        reward = 0

        # 🔻 Time penalty
        reward -= 1

        # 🔹 Start tasks
        for task_id in action.get("start", []):
            if self._can_start(task_id) and self._has_cpu(task_id) and self.tasks[task_id]["status"] == "pending":
                self.tasks[task_id]["status"] = "running"
                self.used_cpu += self.tasks[task_id]["cpu"]
            else:
                reward -= 5  # invalid action

        # 🔹 Simulate time
        self.current_time += 1

        # 🔹 Update running tasks
        for task_id, task in self.tasks.items():
            if task["status"] == "running":
                task["duration"] -= 1

                if task["duration"] <= 0:
                    task["status"] = "done"
                    self.used_cpu -= task["cpu"]

                    reward += task["priority"] * 5

        # 🔹 Idle CPU penalty
        if self.used_cpu < self.total_cpu:
            reward -= 2

        # 🔹 Done check
        if all(t["status"] == "done" for t in self.tasks.values()):
            self.done = True

        return self.state(), reward, self.done

    def _can_start(self, task_id):
        deps = self.dependencies.get(task_id, [])
        return all(self.tasks[d]["status"] == "done" for d in deps)

    def _has_cpu(self, task_id):
        return (self.used_cpu + self.tasks[task_id]["cpu"]) <= self.total_cpu
