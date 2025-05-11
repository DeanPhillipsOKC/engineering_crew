from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool, FileWriterTool
from .models.backend_update import BackendImplementationUpdate
from .tools.update_requirements_file import UpdateRequirementsFileTool

@CrewBase
class FrontendTeam():
    """FrontendTeam crew"""

    agents_config = 'config/frontend_agents.yaml'
    tasks_config = 'config/frontend_tasks.yaml'

    @agent
    def frontend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['frontend_engineer'],
            allow_code_execution=True,
            code_execution_mode='safe',
            tools=[
                FileReadTool(),
                FileWriterTool(),
            ]
        )

    def update_requirements_file(self, inputs):
        tool = UpdateRequirementsFileTool(directory="output/src", force=True)
        output = tool._run()
        print(output)

    @task
    def frontend_task(self) -> Task:
        return Task(
            config=self.tasks_config['frontend_task'],
            output_pydantic=BackendImplementationUpdate,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the research crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )