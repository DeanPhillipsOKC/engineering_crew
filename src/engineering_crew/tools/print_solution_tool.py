from crewai.tools import BaseTool
from pathlib import Path

class PrintPythonFilesTool(BaseTool):
    name: str = "Print Python Files Tool"
    description: str = "Recursively prints all .py files in a directory, showing their paths and contents."

    def _run(self, directory: str) -> str:
        output = []
        py_files = Path(directory).rglob("*.py")
        for file_path in py_files:
            output.append(f"\n=== {file_path} ===")
            try:
                with file_path.open("r", encoding="utf-8") as f:
                    output.append(f.read())
            except Exception as e:
                output.append(f"Error reading {file_path}: {e}")
        return "\n".join(output)
