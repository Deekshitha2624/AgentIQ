# main.py

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.planner_agent import PlannerAgent
from agents.builder_agent import BuilderAgent
from agents.reviewer_agent import ReviewerAgent

from tools.file_tools import FileTools


# ================
# Project Name Maker
# ================
def make_project_name(prompt: str):
    name = "".join(c.lower() if c.isalnum() else "_" for c in prompt)
    while "__" in name:
        name = name.replace("__", "_")
    return name[:40]  # shorter cleaner folder name


# ================
# MAIN LOGIC (no autorun)
# ================
def run_agent(user_prompt: str):
    print("\n=== 🚀 AUTO PROJECT BUILDER (GEMINI POWERED) ===\n")

    planner = PlannerAgent()
    builder = BuilderAgent()
    reviewer = ReviewerAgent()
    file_tools = FileTools()

    # 1. Planning
    print("🧠 PLAN:", planner.plan(user_prompt))

    # 2. Create folder
    project_name = make_project_name(user_prompt)
    project_path = os.path.join("projects", project_name)
    os.makedirs(project_path, exist_ok=True)

    print(f"\n📁 Project folder: {project_path}")

    # 3. Generate project files using Gemini
    print("\n🔧 Calling Gemini API...")
    files, commands = builder.build_files(user_prompt)

    print(f"📄 Gemini generated {len(files)} files")

    # 4. Review
    reviewed_files = reviewer.review(files)

    # 5. Save files into project folder
    print("\n💾 Saving files...")
    print(file_tools.create_files(reviewed_files, project_path))

    # 6. Display helpful message instead of autorun
    
    print("➡️ You can manually run your project using the commands below:")
    print(commands)
    print("\n🎉 DONE! Project is ready in:", project_path, "\n")


if __name__ == "__main__":
    prompt = input("What project do you want me to build? → ")
    run_agent(prompt)
