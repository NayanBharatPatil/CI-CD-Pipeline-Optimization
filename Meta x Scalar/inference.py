from env.environment import PipelineEnv
from agents.baseline_agent import BaselineAgent
from tasks.easy import get_easy_config  

def main():
    try:
        env = PipelineEnv()
        agent = BaselineAgent()

       
        config = get_easy_config()
        state = env.reset(config)

        done = False
        total_reward = 0
        steps = 0

        while not done and steps < 50:
            action = agent.select_action(state)
            state, reward, done = env.step(action)

            total_reward += reward
            steps += 1

        # normalize score
        score = max(0, min(1, total_reward / 100))

        print("Final Score:", score)

    except Exception as e:
        print("Error during inference:", str(e))
        exit(1)

if __name__ == "__main__":
    main()
