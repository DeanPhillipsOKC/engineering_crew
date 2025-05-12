from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool, FileWriterTool
from .memory import long_term_memory, short_term_memory, entity_memory
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

    @agent
    def devops_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['devops_engineer'],
            allow_code_execution=True,
            code_execution_mode='safe',
            tools=[
                FileReadTool(),
                FileWriterTool(),
            ]
        )
    
    @agent
    def scripter(self) -> Agent:
        return Agent(
            config=self.agents_config['scripter'],
            allow_code_execution=True,
            code_execution_mode='safe',
            tools=[
                FileReadTool(),
                FileWriterTool(),
            ]
        )
    
    @agent
    def ux_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['ux_expert'],
            tools=[
                FileReadTool(),
            ]
        )
    
    @agent
    def business_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['business_analyst'],
            tools=[
                FileReadTool(),
            ]
        )

    @agent
    def streamlit_tester(self) -> Agent:
        return Agent(
            config=self.agents_config['streamlit_tester'],
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
            callback=self.update_requirements_file,
        )
    
    @task
    def create_dockerfile_task(self) -> Task:
        return Task(
            config=self.tasks_config['create_dockerfile_task'],
        )

    @task
    def create_bash_run_script_task(self) -> Task:
        return Task(
            config=self.tasks_config['create_bash_run_script_task'],
        )

    @task
    def create_powershsell_run_script_task(self) -> Task:
        return Task(
            config=self.tasks_config['create_powershsell_run_script_task'],
        )
    
    @task
    def create_bash_run_test_script_task(self) -> Task:
        return Task(
            config=self.tasks_config['create_bash_run_test_script_task'],
        )
    
    @task
    def create_powershell_run_test_script_task(self) -> Task:
        return Task(
            config=self.tasks_config['create_powershell_run_test_script_task'],
        )

    @task
    def review_ux_task(self) -> Task:
        return Task(
            config=self.tasks_config['review_ux_task'],
        )
    
    @task
    def implement_ux_suggestions_task(self) -> Task:
        return Task(
            config=self.tasks_config['implement_ux_suggestions_task'],
        )

    @task
    def identify_use_cases_task(self) -> Task:
        return Task(
            config=self.tasks_config['identify_use_cases_task'],
        )

    @task
    def test_streamlit_ui_task(self) -> Task:
        return Task(
            config=self.tasks_config['test_streamlit_ui_task'],
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