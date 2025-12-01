# tools/exec_tools.py

import subprocess
import platform

class ExecTools:
    def run_command(self, command: str):
        try:
            # Fix "open file" for Windows → convert to "start file"
            if command.startswith("open "):
                if platform.system().lower() == "windows":
                    file = command.replace("open ", "").strip()
                    command = f"start {file}"

            result = subprocess.check_output(
                command, shell=True, text=True
            )
            return result

        except Exception as e:
            return f"❌ Command failed: {e}"
