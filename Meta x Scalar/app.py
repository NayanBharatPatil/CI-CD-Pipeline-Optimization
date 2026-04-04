from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from agents.baseline_agent import BaselineAgent
from env.environment import PipelineEnv
from tasks.easy import get_easy_config
from tasks.medium import get_medium_config
from tasks.hard import get_hard_config

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


def run_simulation(config):
    env = PipelineEnv()
    agent = BaselineAgent()

    state = env.reset(config)

    done = False
    steps = 0
    total_reward = 0

    logs = []

    while not done and steps < 20:
        action = agent.select_action(state)
        state, reward, done = env.step(action)

        logs.append({
            "step": steps,
            "reward": reward
        })

        total_reward += reward
        steps += 1

    score = max(0, min(1, total_reward / 100))

    return {
        "steps": steps,
        "score": round(score, 2),
        "logs": logs
    }


@app.get("/run/easy")
def run_easy():
    return run_simulation(get_easy_config())


@app.get("/run/medium")
def run_medium():
    return run_simulation(get_medium_config())


@app.get("/run/hard")
def run_hard():
    return run_simulation(get_hard_config())