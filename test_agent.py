from agents.orchestrator import run_dynamic_agent

# Test the agent
result = run_dynamic_agent("What is the stock price of AAPL?", "AAPL")
print("Result:", result)