from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff
from crewai_tools import FileReadTool, FileWriterTool
from .models.design import Design
from .models.backlog import Backlog
from .models.backend_update import BackendImplementationUpdate
from .models.test_update import TestImplementationUpdate
import os
import shutil

@CrewBase
class DevelopmentTeam():
    """DevelopmentTeam crew"""

    agents_config = 'config/development_agents.yaml'
    tasks_config = 'config/development_tasks.yaml'

    @agent
    def backend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['backend_engineer'],
            verbose=True,
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
            verbose=True,
            allow_code_execution=True,
            code_execution_mode='safe',
            tools=[
                FileReadTool(),
                FileWriterTool(),
            ]
        )

    @task
    def code_task(self) -> Task:
        return Task(
            config=self.tasks_config['code_task'],
            output_pydantic=BackendImplementationUpdate,
        )
    
    @task
    def test_task(self) -> Task:
        return Task(
            config=self.tasks_config['test_task'],
            output_pydantic=TestImplementationUpdate,
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