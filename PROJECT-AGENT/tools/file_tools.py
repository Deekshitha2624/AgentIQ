# tools/file_tools.py

import os

class FileTools:
    def create_files(self, files: dict, output_folder: str):
        for path, content in files.items():
            full_path = os.path.join(output_folder, path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)

        return f"Created {len(files)} files in {output_folder}"
