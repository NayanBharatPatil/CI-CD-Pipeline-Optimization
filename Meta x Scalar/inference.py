import os
from openai import OpenAI

from env.environment import PipelineEnv
from agents.baseline_agent import BaselineAgent
from tasks.easy import get_easy_config

def call_llm():
    try:
        client = OpenAI(
            base_url=os.environ["API_BASE_URL"],
            api_key=os.environ["API_KEY"]
        )

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Optimize CI/CD pipeline"}
            ],
            max_tokens=10
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"LLM error: {str(e)}"


def main():
    try:
        env = PipelineEnv()
        agent = BaselineAgent()

        config = get_easy_config()
        state = env.reset(config)

        done = False
        total_reward = 0
        steps = 0

        print("[START] task=easy", flush=True)

        while not done and steps < 50:
            action = agent.select_action(state)
            state, reward, done = env.step(action)

            steps += 1
            total_reward += reward

            print(f"[STEP] step={steps} reward={reward}", flush=True)

        
        llm_output = call_llm()

        score = max(0, min(1, total_reward / 100))

        print(f"[END] task=easy score={round(score, 2)} steps={steps}", flush=True)

    except Exception as e:
        print(f"[ERROR] {str(e)}", flush=True)
        exit(1)


if __name__ == "__main__":
    main()
