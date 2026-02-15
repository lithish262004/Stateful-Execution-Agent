import streamlit as st
from agent import start_goal, execute_next, get_status, reset_memory

st.title("WorkElate Stateful Execution Agent")

if "plan" not in st.session_state:
    st.session_state.plan = []

goal = st.text_input("Enter your goal")

if st.button("Start Goal"):
    if goal:
        plan = start_goal(goal)
        st.session_state.plan = plan
        st.success("Plan created successfully!")

if st.session_state.plan:
    st.subheader("Execution Plan")
    for step in st.session_state.plan:
        st.write("-", step)

if st.button("Execute Next Step"):
    result = execute_next()
    st.success(result)

if st.button("Show Status"):
    status = get_status()
    st.json(status)

if st.button("Reset Agent"):
    reset_memory()
    st.session_state.plan = []
    st.warning("Agent reset.")
