import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.baseline_agent import BaselineAgent
from env.environment import PipelineEnv
from tasks.easy import get_easy_config
# from tasks.medium import get_medium_config
# from tasks.hard import get_hard_config

env = PipelineEnv()
agent = BaselineAgent()

# 🔹 Choose task here
config = get_easy_config()
# config = get_medium_config()
# config = get_hard_config()

state = env.reset(config)

done = False
steps = 0
max_steps = 20
total_reward = 0

print("🚀 Starting Pipeline Simulation\n")

while not done and steps < max_steps:

    action = agent.select_action(state)

    state, reward, done = env.step(action)

    total_reward += reward

    print(f"Step: {steps}")
    print("Action:", action)
    print("Reward:", reward)
    print("CPU:", state["cpu"])
    print("Tasks:", state["tasks"])
    print("--------------")

    steps += 1

# 🔚 Final result
if done:
    print("✅ Pipeline completed!")
else:
    print("⚠️ Stopped early")

print(f"⏱️ Steps: {steps}")

# 🔹 Score calculation
max_possible = 100
score = max(0, min(1, total_reward / max_possible))

print(f"🎯 Score: {score:.2f}")