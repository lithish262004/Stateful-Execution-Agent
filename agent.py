import json
import os
from mistralai import Mistral
import os

client = Mistral(api_key="AKbidp4tSyib6S1eotVw1O1DnFTudSCX")


MEMORY_FILE = "memory.json"

DEFAULT_MEMORY = {
    "goal": "",
    "plan": [],
    "completed_steps": [],
    "current_step": 0,
    "history": []
}


# ======= MEMORY FUNCTIONS =======

def load_memory():
    try:
        if not os.path.exists(MEMORY_FILE):
            save_memory(DEFAULT_MEMORY)
            return DEFAULT_MEMORY

        if os.path.getsize(MEMORY_FILE) == 0:
            save_memory(DEFAULT_MEMORY)
            return DEFAULT_MEMORY

        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except:
        save_memory(DEFAULT_MEMORY)
        return DEFAULT_MEMORY


def save_memory(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ======= PLANNER (LLM) =======
def create_plan(goal):
    prompt = f"""
You are an AI execution planner.

Break the following goal into 5 specific operational steps.

Rules:
- Steps must be real actionable work
- Avoid generic steps like understand, analyze, execute tasks
- Make steps domain-specific and practical

Goal: {goal}

Return only numbered steps.
"""

    try:
        response = client.chat.complete(
            model="mistral-small-latest",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        text = response.choices[0].message.content

        steps = []
        for line in text.split("\n"):
            line = line.strip()
            if line and line[0].isdigit():
                steps.append(line.split(".", 1)[-1].strip())

        if len(steps) < 3:
            raise Exception("Weak output")

        return steps[:5]

    except Exception as e:
        print("Mistral failed, using fallback:", e)
        return fallback_plan(goal)


# ======= AGENT OPERATIONS =======

def start_goal(goal):
    memory = {
        "goal": goal,
        "plan": create_plan(goal),
        "completed_steps": [],
        "current_step": 0,
        "history": []
    }

    memory["history"].append({
        "event": "goal_started",
        "goal": goal
    })

    save_memory(memory)
    return memory["plan"]



def execute_next():
    memory = load_memory()

    if memory["current_step"] >= len(memory["plan"]):
        return "All steps completed."

    step = memory["plan"][memory["current_step"]]

    reasoning = f"Step {memory['current_step']+1} is required to progress toward the goal."

    # FIX: Add this line
    memory["completed_steps"].append(step)

    memory["history"].append({
        "event": "step_executed",
        "step": step,
        "reason": reasoning
    })

    memory["current_step"] += 1
    save_memory(memory)

    next_task = None
    if memory["current_step"] < len(memory["plan"]):
        next_task = memory["plan"][memory["current_step"]]

    return f"""
Completed: {step}
Reason: {reasoning}
Next Task: {next_task}
Progress: {memory['current_step']}/{len(memory['plan'])}
"""


def get_status():
    return load_memory()


def reset_memory():
    save_memory(DEFAULT_MEMORY)

def fallback_plan(goal):
    return [
        f"Define detailed requirements for: {goal}",
        "Design implementation approach",
        "Build core functionality",
        "Test and refine the solution",
        "Deploy and complete execution"
    ]

