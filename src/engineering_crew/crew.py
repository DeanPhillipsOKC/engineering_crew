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

    def assign_to_backend_engineer(self) -> Task:
        return Task(
            description="Assign the next uncompleted task to the backend engineer.",
            expected_output="The engineering task assigned to the backend engineer.",
            output_pydantic=EngineeringTask,
            agent=self.engineering_lead(),
        )

    def on_tasks_created(self, output):
        print("*** Adding Task ***")
        #self.tasks.append(self.assign_to_backend_engineer())
        return self.assign_to_backend_engineer()

    @task
    def task_creation_task(self) -> Task:
        return Task(
            config=self.tasks_config['task_creation_task'],
            output_pydantic=EngineeringTasks,
            callback=self.on_tasks_created
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
        )