from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff
from crewai_tools import FileReadTool, FileWriterTool, CodeInterpreterTool
from pydantic import BaseModel
from .models.design import Design, DesignModule
from .services.tasks import TaskManager
import os
import shutil

@CrewBase
class EngineeringTeam():
    """EngineeringTeam crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    task_manager = None

    @before_kickoff
    def reset_output(self, _):
        shutil.rmtree("output", ignore_errors=True)
        os.makedirs("output/src", exist_ok=True)


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
            tools=[
                FileReadTool(),
                FileWriterTool(),
                CodeInterpreterTool(result_as_answer=True)
            ]
        )

    def on_module_implemented(self, result):
        next_task = self.task_manager.pop_module()

        if next_task:
            self.create_implement_module_task(next_task)

    def create_implement_module_task(self, module: DesignModule) -> Task:
        # convert the module pydantic object to a string
        module_str = module.model_dump_json(indent=2)

        design = self.task_manager.get_design()
        task = Task(
            description=f"Implement the module, methods, and fields.  Write them to the output/src folder \
                never finish the task without executing the code first.  If you get errors due to missing \
                modules, create a stub for the module and write it to the output/src folder. \
                \
                MODULE TO IMPLEMENT: {module_str} \
                \
                REQUIREMENTS: {design.requirements} \
                \
                ARCHITECTURE STANDARDS: {design.architecture_standards} \
                \
                FOLDER STRUCTURE: {design.folder_structure} \
                \
                BEST PRACTICES: {design.best_practices}",
            expected_output="A python module that implements the design and achieves the requirements. \
                            IMPORTANT: Output ONLY the raw Python code without any markdown formatting, code \
                            block delimiters, or backticks. The output should be valid Python code that can \
                            be directly saved to a file and executed.",
            agent=self.backend_engineer(),
            callback=self.on_module_implemented,
            output_file=f"output/src/{module.file_path}",
        )
        result = task.execute_sync()

    def on_design_created(self, result):
        self.task_manager = TaskManager(result.pydantic)
        self.create_implement_module_task(self.task_manager.pop_module())

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