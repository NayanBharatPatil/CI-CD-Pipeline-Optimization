class BaselineAgent:

    def select_action(self, state):
        tasks = state["tasks"]
        total_cpu = state["cpu"]["total"]
        used_cpu = state["cpu"]["used"]

        available_cpu = total_cpu - used_cpu

        candidates = []

        # 🔹 Get pending tasks
        for task_id, task in tasks.items():
            if task["status"] == "pending":
                candidates.append((task_id, task))

        # 🔹 Sort by priority
        candidates.sort(key=lambda x: x[1]["priority"], reverse=True)

        selected = []

        # 🔹 Select tasks within CPU limit
        for task_id, task in candidates:
            if task["cpu"] <= available_cpu:
                selected.append(task_id)
                available_cpu -= task["cpu"]

        return {"start": selected}