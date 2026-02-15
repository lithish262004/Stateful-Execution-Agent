WorkElate – Stateful Execution Agent

Overview
This project implements a Stateful Execution Agent that plans, executes, remembers, and continues tasks over time.
The system demonstrates how AI can function as an operational worker layer, not just a chatbot.

Key Features
1. Goal-Driven Planning
User provides a goal
Planning is generated using Mistral LLM
Steps are:
Operational
Domain-aware
Actionable


2. Stateful Memory

All execution state is stored in memory.json:
Current goal
Execution plan
Completed step
Current step index
Decision history

This allows:
Continuation across sessions
Persistent reasoning context

3. Worker-like Execution
The agent behaves like a worker:
Executes one step at a time
User triggers Execute Next Step
Tracks progress incrementally
Stops when goal is completed

4. Decision Trace & Transparency
Each action is logged:
event: step_executed
step: Design system architecture
reason: Required to progress toward goal

This creates a full decision history for transparency.

5. Reliability
Uses Mistral API for planning
Includes fallback operational planner if LLM fails
Ensures deterministic execution
Architecture

User Input
→ Planning Layer (Mistral)
→ Execution Controller
→ Memory Layer (JSON)
→ Streamlit Interface

Flow:

Planning → Action → Memory → Continuation
Real-World Use Case
Product launch planning
Intern onboarding workflows
Marketing execution
Investor reporting preparation

How to Run
pip install streamlit mistralai
streamlit run app.py


Add your API key in agent.py.
