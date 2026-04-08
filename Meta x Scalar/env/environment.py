class PipelineEnv:
    def __init__(self):
        self.tasks = {}
        self.dependencies = {}
        self.total_cpu = 4
        self.used_cpu = 0
        self.time = 0

    def reset(self, config=None):
        if config is None:
            raise ValueError("Config must be provided")

        self.tasks = {
            task_id: {
                "status": "pending",
                "duration": task["duration"],
                "cpu": task["cpu"]
            }
            for task_id, task in config["tasks"].items()
        }

        self.dependencies = config.get("dependencies", {})
        self.total_cpu = config.get("total_cpu", 4)

        self.used_cpu = 0
        self.time = 0

        return self.state()

    def state(self):
        return {
            "tasks": self.tasks,
            "time": self.time,
            "cpu": {
                "total": self.total_cpu,
                "used": self.used_cpu
            }
        }

    def step(self, action):
        reward = 0

        for task_id in action.get("start", []):
            if (
                self.tasks[task_id]["status"] == "pending"
                and self._can_start(task_id)
                and self._has_cpu(task_id)
            ):
                self.tasks[task_id]["status"] = "running"
                self.used_cpu += self.tasks[task_id]["cpu"]

        for task_id, task in self.tasks.items():
            if task["status"] == "running":
                task["duration"] -= 1

                if task["duration"] <= 0:
                    task["status"] = "done"
                    self.used_cpu -= task["cpu"]
                    reward += 10  


        self.time += 1

      
        done = all(task["status"] == "done" for task in self.tasks.values())

        
        reward -= 1

        return self.state(), reward, done

    def _can_start(self, task_id):
        deps = self.dependencies.get(task_id, [])
        return all(self.tasks[d]["status"] == "done" for d in deps)

    def _has_cpu(self, task_id):
        return (self.used_cpu + self.tasks[task_id]["cpu"]) <= self.total_cpu
