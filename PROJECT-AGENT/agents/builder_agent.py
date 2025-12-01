# agents/builder_agent.py

import os
import json
from dotenv import load_dotenv
from google import genai

class BuilderAgent:
    def __init__(self):
        load_dotenv()

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("❌ GEMINI_API_KEY missing in .env")

        self.client = genai.Client(api_key=api_key)

    def build_files(self, user_request: str):
        """
        Calls Gemini API and returns:
        - files (dict)
        - commands (list)
        """

        prompt = f"""
        You are an AI project bootstrap generator.
        Based on this request:

        "{user_request}"

        Generate a COMPLETE project and ALWAYS include run commands.

        Return ONLY raw JSON in this EXACT structure:

        {{
          "files": {{
            "path/to/file1": "file content",
            "folder/another_file": "content"
          }},
          "dependencies": ["list","of","packages"],
          "commands": [
            "command to install dependencies",
            "command to run the project"
          ]
        }}

        RULES:
        • "commands" MUST contain AT LEAST ONE command.
        • For Python projects ALWAYS include "python app.py" or "python main.py".
        • For Node.js ALWAYS include "node index.js".
        • For React/Vite ALWAYS include "npm install" + "npm run dev".
        • DO NOT return markdown.
        • DO NOT add explanations.
        • ONLY JSON.
        """

        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config={"response_mime_type": "application/json"},
        )

        output = json.loads(response.text)

        files = output.get("files", {})
        commands = output.get("commands", [])

        # ============================
        # FALLBACK AUTORUN LOGIC
        # ============================

        if not commands:
            commands = []

            # Python Flask / normal Python
            if "app.py" in files:
                commands.append("pip install flask")
                commands.append("python output_project/app.py")

            elif "main.py" in files:
                commands.append("python output_project/main.py")

            # Node.js
            elif "index.js" in files:
                commands.append("npm install")
                commands.append("node output_project/index.js")

            # React
            elif "package.json" in files:
                commands.append("npm install")
                commands.append("npm run dev")

            # Nothing matched
            if not commands:
                commands.append("echo 'No autorun command detected.'")

        return files, commands
