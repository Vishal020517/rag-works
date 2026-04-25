# from agents.orchestrator import run_full_analysis

# result = run_full_analysis("TSLA")
# # print(result)
# from agents.planner_agent import planner_agent

# plan=planner_agent("Should I buy Tesla?")
# print(plan)

from agents.orchestrator import run_dynamic_agent

result = run_dynamic_agent(
    "Should I invest in Tesla?",
    "TSLA"
)

print(result)