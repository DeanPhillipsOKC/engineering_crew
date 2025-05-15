import os
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

class FileSearchToolInput(BaseModel):
    filename: str = Field(..., description="The name of the file to search for (e.g., 'main.py').")

class FileSearchTool(BaseTool):
    name: str = "File Search Tool"
    description: str = "Finds the full relative path of a file inside the output/src directory. \
        This is useful for locating files in the project structure."
    args_schema: type = FileSearchToolInput

    def _run(self, filename: str) -> str:
        base_dir = "output/src"
        for root, dirs, files in os.walk(base_dir):
            if filename in files:
                full_path = os.path.join(root, filename)
                return full_path.replace("\\", "/")  # Ensure consistent path format
        return f"File '{filename}' not found in {base_dir}"
