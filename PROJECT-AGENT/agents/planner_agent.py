# agents/planner_agent.py

class PlannerAgent:
    def plan(self, user_prompt: str):
        return [
            "Analyze request",
            "Ask Gemini to generate project",
            "Receive JSON structure",
            "Create files",
            "Finish"
        ]
