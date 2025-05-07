from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool, FileWriterTool
from .tools.tasks import AddTaskTool, ListTasksTool
from pydantic import BaseModel

class EngineeringTask(BaseModel):
    id: str
    description: str
    completed: bool = False

class EngineeringTasks(BaseModel):
    tasks: list[EngineeringTask]

@CrewBase
class EngineeringTeam():
    """EngineeringTeam crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def engineering_lead(self) -> Agent:
        return Agent(
            config=self.agents_config['engineering_lead'],
            verbose=True,
            tools=[
                AddTaskTool(),
                ListTasksTool(),
            ],
        )

    @agent
    def backend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['backend_engineer'],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",  # Uses Docker for safety
            max_execution_time=120, 
            max_retry_limit=3,
            tools=[
                FileReadTool(),
                FileWriterTool(),
            ]
        )

    @task
    def design_task(self) -> Task:
        return Task(
            config=self.tasks_config['design_task']
        )

    @task
    def task_creation_task(self) -> Task:
        return Task(
            config=self.tasks_config['task_creation_task'],
            output_pydantic=EngineeringTasks,
        )

    @task
    def recommend_next_task_task(self) -> Task:
        return Task(
            config=self.tasks_config['recommend_next_task_task']
        )

    @task
    def implement_task_task(self) -> Task:
        return Task(
            config=self.tasks_config['implement_task_task'],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the research crew"""

        task_manager = Agent(
            config=self.agents_config['task_manager'],
            allow_delegation=True
        )

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.hierarchical,
            manager_agent=task_manager,
            verbose=True,
            memory=True,
        )