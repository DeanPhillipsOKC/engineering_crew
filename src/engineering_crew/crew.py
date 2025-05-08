from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool, FileWriterTool
from pydantic import BaseModel

class DesignField(BaseModel):
    name: str
    description: str
    requirements: str

class DesignMethod(BaseModel):
    name: str
    description: str
    prototype: str
    requirements: str

class DesignModule(BaseModel):
    name: str
    description: str
    requirements: str
    methods: list[DesignMethod]
    fields: list[DesignField]

class Design(BaseModel):
    modules: list[DesignModule]

@CrewBase
class EngineeringTeam():
    """EngineeringTeam crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def engineering_lead(self) -> Agent:
        return Agent(
            config=self.agents_config['engineering_lead'],
            verbose=True
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

    def assign_to_backend_engineer(self, design: Design) -> Task:
        task = Task(
            description="Implement the modules, methods, and fields.  Write them to the output/src folder",
            expected_output="The module source code written to the output/src folder.",
            agent=self.backend_engineer(),
            scope=design.modules[0]
        )
        print("*** Appended ***")
        result = task.execute_sync()

    def on_design_created(self, result):
        print("*** Adding Task ***")
        #self.tasks.append(self.assign_to_backend_engineer())
        return self.assign_to_backend_engineer(result.pydantic)

    @task
    def design_task(self) -> Task:
        return Task(
            config=self.tasks_config['design_task'],
            callback=self.on_design_created,
            output_pydantic=Design,
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