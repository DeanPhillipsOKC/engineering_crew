from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff
from .tools.update_requirements_file import UpdateRequirementsFileTool
import shutil
import os


@CrewBase
class EngineeringTeam():
    """EngineeringTeam crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @before_kickoff
    def on_before_kickoff(self, inputs):
        # Delete the output directory if it exists
        shutil.rmtree('output', ignore_errors=True)
        os.makedirs('output/src', exist_ok=True)

        # Copy the contents of the assets directory to the output/src directory
        shutil.copytree('assets', 'output/src', dirs_exist_ok=True)

        return inputs

    @agent
    def engineering_lead(self) -> Agent:
        return Agent(
            config=self.agents_config['engineering_lead'],
            verbose=True,
        )

    @agent
    def backend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['backend_engineer'],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",  # Uses Docker for safety
            max_execution_time=120, 
            max_retry_limit=3 
        )
    
    @agent
    def frontend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['frontend_engineer'],
            verbose=True,
        )
    
    @agent
    def test_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['test_engineer'],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",  # Uses Docker for safety
        )
    
    @agent
    def streamlit_tester(self) -> Agent:
        return Agent(
            config=self.agents_config['streamlit_tester'],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",  # Uses Docker for safety
        )

    def update_requirements_file(self, inputs):
        tool = UpdateRequirementsFileTool(directory="output/src", force=True)
        output = tool._run()
        print(output)

    @task
    def design_task(self) -> Task:
        return Task(
            config=self.tasks_config['design_task']
        )

    @task
    def code_task(self) -> Task:
        return Task(
            config=self.tasks_config['code_task'],
            callback=self.update_requirements_file,
        )

    @task
    def frontend_task(self) -> Task:
        return Task(
            config=self.tasks_config['frontend_task'],
            callback=self.update_requirements_file,
        )

    @task
    def test_task(self) -> Task:
        return Task(
            config=self.tasks_config['test_task'],
            callback=self.update_requirements_file,
        )   

    @task
    def streamlit_test_task(self) -> Task:
        return Task(
            config=self.tasks_config['streamlit_test_task'],
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