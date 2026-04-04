from env.environment import PipelineEnv
from agents.baseline_agent import BaselineAgent

env = PipelineEnv()
agent = BaselineAgent()

state = env.reset()

done = False
total_reward = 0

while not done:
    action = agent.select_action(state)
    state, reward, done = env.step(action)
    total_reward += reward

score = max(0, min(1, total_reward / 100))

print("Final Score:", score)