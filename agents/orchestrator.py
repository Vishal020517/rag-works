from agents.planner_agent import planner_agent
from agents.tool_registry import TOOLS

def run_dynamic_agent(query: str, ticker: str):
    try:
        print("🧠 Dynamic Agent Started")

        plan = planner_agent(query)

        # Context (shared memory)
        ctx = {
            "ticker": ticker
        }

        # Execute steps dynamically
        for step_obj in plan:
            step = step_obj["step"]

            print(f"⚙️ Executing: {step}")

            if step in TOOLS:
                ctx = TOOLS[step](ctx)
            else:
                print(f"⚠️ Unknown step: {step}")

        print("✅ Execution completed")

        return ctx

    except Exception as e:
        return {
            "error": "Dynamic execution failed",
            "details": str(e)
        }