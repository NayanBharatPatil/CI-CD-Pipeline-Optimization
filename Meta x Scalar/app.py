from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from typing import Dict

from env.environment import PipelineEnv
from agents.baseline_agent import BaselineAgent
from tasks.easy import get_easy_config
from tasks.medium import get_medium_config
from tasks.hard import get_hard_config

app = FastAPI()

# Global env for OpenEnv API
current_env = None

# ----------------------------
# 🔥 SIMPLE UI (WORKING)
# ----------------------------
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>CI/CD Pipeline Optimizer</title>
    <style>
        body {
            font-family: Arial;
            text-align: center;
            background: #0f172a;
            color: white;
        }
        button {
            padding: 10px 20px;
            margin: 10px;
            font-size: 16px;
            border-radius: 8px;
            cursor: pointer;
        }
        .easy { background: green; }
        .medium { background: orange; }
        .hard { background: red; }
        #output {
            margin-top: 20px;
            background: #1e293b;
            padding: 20px;
            border-radius: 10px;
            width: 80%;
            margin-left: auto;
            margin-right: auto;
            text-align: left;
            white-space: pre-wrap;
        }
    </style>
</head>
<body>

<h1>🚀 CI/CD Pipeline Optimization</h1>

<button class="easy" onclick="runTask('easy')">Easy</button>
<button class="medium" onclick="runTask('medium')">Medium</button>
<button class="hard" onclick="runTask('hard')">Hard</button>

<div id="output">Click a button to run simulation...</div>

<script>
async function runTask(level) {
    document.getElementById("output").innerText = "Running...";

    const res = await fetch(`/run/${level}`);
    const data = await res.json();

    let text = `Steps: ${data.steps}\\nScore: ${data.score}\\n\\n`;

    data.logs.forEach(log => {
        text += `Step ${log.step} | Reward: ${log.reward}\\n`;
    });

    document.getElementById("output").innerText = text;
}
</script>

</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def home():
    return HTML_PAGE


# ----------------------------
# 🔥 OpenEnv APIs (FIXED FORMAT)
# ----------------------------

@app.post("/reset")
def reset_env():
    global current_env
    current_env = PipelineEnv()

    state = current_env.reset()

    return {
        "observation": state,
        "info": {}
    }


@app.post("/step")
def step_env(action: Dict):
    global current_env

    if current_env is None:
        return {"error": "Call /reset first"}

    state, reward, done = current_env.step(action)

    return {
        "observation": state,
        "reward": reward,
        "done": done,
        "info": {}
    }


@app.get("/state")
def get_state():
    global current_env

    if current_env is None:
        return {"error": "Not initialized"}

    return {
        "observation": current_env.state()
    }


# ----------------------------
# 🔥 SIMULATION (UI)
# ----------------------------

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


# ----------------------------
# 🔥 UI ROUTES
# ----------------------------

@app.get("/run/easy")
def run_easy():
    return run_simulation(get_easy_config())


@app.get("/run/medium")
def run_medium():
    return run_simulation(get_medium_config())


@app.get("/run/hard")
def run_hard():
    return run_simulation(get_hard_config())
