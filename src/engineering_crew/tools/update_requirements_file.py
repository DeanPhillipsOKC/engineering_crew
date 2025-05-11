import subprocess
from crewai.tools import BaseTool
from pydantic import Field

class UpdateRequirementsFileTool(BaseTool):
    name: str = "Update Requirements File Tool"
    description: str = "Generates requirements.txt using pipreqs based on actual imports."

    directory: str = Field(default="output/src")
    save_path: str = Field(default=None)
    force: bool = Field(default=False)

    def _run(self) -> str:
        command = ["pipreqs", self.directory]
        if self.save_path:
            command.extend(["--savepath", self.save_path])
        if self.force:
            command.append("--force")
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"pipreqs failed: {result.stderr}")
        return result.stdout
