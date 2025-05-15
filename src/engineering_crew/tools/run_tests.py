from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import docker
import os

class RunTestsToolOutput(BaseModel):
    passed: bool
    logs: str


class RunTestsTool(BaseTool):
    name: str = "Run Tests Tool"
    description: str = (
        "Builds a Docker image  and runs tests inside a container."
    )

    def _run(self) -> RunTestsToolOutput:
        try:
            dockerfile_path = "output/src/Dockerfile.tests"
            image_tag = "pytest_runner"
            source_dir = "output/src"
            test_command = "python -m pytest"

            client = docker.from_env()

            print("Files in output/src:")
            print(os.listdir('output/src'))

            # Build the Docker image
            print(f"Building Docker image '{image_tag}' from '{dockerfile_path}'...")
            image, build_logs = client.images.build(
                path=os.path.dirname(dockerfile_path),
                dockerfile=os.path.basename(dockerfile_path),
                tag=image_tag,
                rm=True
            )

            # Run the container with the source directory mounted
            print(f"Running container from image '{image_tag}'...")
            container = client.containers.run(
                image=image_tag,
                command=test_command,
                volumes={
                    os.path.abspath(source_dir): {
                        'bind': '/app',
                        'mode': 'rw'
                    }
                },
                working_dir="/app",
                detach=True
            )

            # Wait for the container to finish and capture logs
            result = container.wait()
            logs = container.logs().decode('utf-8')
            container.remove()

            if result['StatusCode'] == 0 or result['StatusCode'] == 5:
                return RunTestsToolOutput(passed=True, logs=logs)
            else:
                return RunTestsToolOutput(passed=False, logs=logs)

        except docker.errors.BuildError as build_err:
            return f"❌ Docker build failed: {str(build_err)}"
        except docker.errors.ContainerError as container_err:
            return f"❌ Container execution failed: {str(container_err)}"
        except Exception as e:
            return f"❌ An unexpected error occurred: {str(e)}"
