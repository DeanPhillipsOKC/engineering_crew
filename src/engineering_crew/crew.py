from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool, FileWriterTool
from .tools.tasks import AddTaskTool, ListTasksTool, CompleteTaskTool, GetNextActiveTaskTool
from pydantic import BaseModel

class DesignMethod(BaseModel):
    name: str
    description: str
    prototype: str

class DesignField(BaseModel):
    name: str
    type: str
    description: str

class DesignClass(BaseModel):
    name: str
    description: str
    methods: list[DesignMethod]
    fields: list[DesignField]

class DesignModule(BaseModel):
    name: str
    description: str
    classes: list[DesignClass]

class DesignModules(BaseModel):
    modules: list[DesignModule]

@CrewBase
class EngineeringTeam():
    """EngineeringTeam crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def software_architect(self) -> Agent:
        return Agent(
            config=self.agents_config['software_architect'],
        )

    @agent
    def backend_developer(self) -> Agent:
        return Agent(
            config=self.agents_config['backend_developer'],
            tools=[
                FileReadTool(),
                FileWriterTool()
            ],
            allow_code_execution=True,
            code_execution_mode="safe"
        )

    @task
    def design_task(self) -> Task:
        return Task(
            config=self.tasks_config['design_task'],
            pydantic_model=DesignModules,
        )
    
    @task
    def implement_backend_code_task(self) -> Task:
        return Task(
            config=self.tasks_config['implement_backend_code_task']
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