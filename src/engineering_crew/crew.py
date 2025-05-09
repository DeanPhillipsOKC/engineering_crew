from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff
from crewai_tools import FileReadTool, FileWriterTool
import os
import shutil
from pydantic import BaseModel

class RefactoringGuidance(BaseModel):
    """Refactoring guidance for the code"""
    code_is_good_enough: bool
    suggestion: str

@CrewBase
class EngineeringTeam():
    """EngineeringTeam crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @before_kickoff
    def purge_output_folders(self, inputs):
        """Purge the output folders"""
        shutil.rmtree('output', ignore_errors=True)
        os.makedirs('output', exist_ok=True)

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
            max_execution_time=120, 
            max_retry_limit=3 
        )

    @agent
    def devops_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['devops_engineer'],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",  # Uses Docker for safety
            max_execution_time=120, 
            max_retry_limit=3 
        )

    @agent
    def refactoring_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['refactoring_engineer'],
            verbose=True,
            tools=[FileReadTool()]
        )

    @task
    def design_task(self) -> Task:
        return Task(
            config=self.tasks_config['design_task']
        )

    @task
    def code_task(self) -> Task:
        return Task(
            config=self.tasks_config['code_task'],
        )

    @task
    def frontend_task(self) -> Task:
        return Task(
            config=self.tasks_config['frontend_task'],
        )

    @task
    def test_task(self) -> Task:
        return Task(
            config=self.tasks_config['test_task'],
        )   
    
    @task
    def dependencies_task(self) -> Task:
        return Task(
            config=self.tasks_config['dependencies_task'],
        )
    
    @task
    def containerize_task(self) -> Task:
        return Task(
            config=self.tasks_config['containerize_task'],
        )
    
    @task
    def bash_script_task(self) -> Task:
        return Task(
            config=self.tasks_config['bash_script_task'],
        )

    @task
    def powershell_script_task(self) -> Task:
        return Task(
            config=self.tasks_config['powershell_script_task']
        )

    @task
    def make_refactoring_recommendation_task(self) -> Task:
        return Task(
            config=self.tasks_config['make_refactoring_recommendation_task'],
            output_pydantic=RefactoringGuidance
        )

    @task
    def implement_refactoring_recommendation_task(self) -> Task:
        return Task(
            config=self.tasks_config['implement_refactoring_recommendation_task'],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the research crew"""
        manager = Agent(
            role="Project Manager",
            goal="Create a working product by leveraging the unique skills of each agent.  Never stop until the refactoring" \
            "engineer is satisified with the code and indicates that no further refactoring is needed.",
            backstory="You are the project manager of a team of engineers.  You will be responsible for assigning tasks to the engineers.",
            allow_delegation=True,
            verbose=True,
        )

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.hierarchical,
            manager_agent=manager,
            verbose=True,
        )