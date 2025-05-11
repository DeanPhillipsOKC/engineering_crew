from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff
from crewai_tools import FileReadTool, FileWriterTool
from .memory import long_term_memory, short_term_memory, entity_memory
from .models.design import Design
from .models.backlog import Backlog
from .models.backend_update import BackendImplementationUpdate
from .models.test_update import TestImplementationUpdate
from .tools.update_requirements_file import UpdateRequirementsFileTool
import os
import shutil

@CrewBase
class BackendTeam():
    """BackendTeam crew"""

    agents_config = 'config/backend_agents.yaml'
    tasks_config = 'config/backend_tasks.yaml'

    @agent
    def backend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['backend_engineer'],
            allow_code_execution=True,
            code_execution_mode='safe',
            tools=[
                FileReadTool(),
                FileWriterTool(),
            ]
        )
    
    @agent
    def test_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['test_engineer'],
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
    def code_task(self) -> Task:
        return Task(
            config=self.tasks_config['code_task'],
            output_pydantic=BackendImplementationUpdate,
            callback=self.update_requirements_file,
        )

    @task
    def test_task(self) -> Task:
        return Task(
            config=self.tasks_config['test_task'],
            output_pydantic=TestImplementationUpdate,
            callback=self.update_requirements_file,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the research crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            memory=True,
            long_term_memory=long_term_memory,
            short_term_memory=short_term_memory,
            entity_memory=entity_memory,
        )