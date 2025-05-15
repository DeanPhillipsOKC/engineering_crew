from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff
from crewai_tools import FileReadTool, FileWriterTool
from .memory import short_term_memory
from .tools.update_requirements_file import UpdateRequirementsFileTool
from .tools.run_tests import RunTestsTool
from .tools.file_search_tool import FileSearchTool
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

    def fix_test_failures(self, logs):
        task = Task(
            description=f"Fix the test failures from the logs \
                The Logs: \
                {logs}",
            expected_output="The test failures have been fixed by updating the code \
                and / or tests in the ouput/src directory.",
            agent=self.backend_engineer(),
            callback=self.run_tests
        )
        result = task.execute_sync()

    test_failures_since_last_success = 0
    TEST_FAILURE_THRESHOLD = 10

    def run_tests(self, inputs):
        if self.test_failures_since_last_success >= self.TEST_FAILURE_THRESHOLD:
            # throw exception
            raise Exception("Test failures exceeded the threshold.")
        
        result = RunTestsTool().run()

        if result.passed:
            print("*** All tests passed. ***")
            print(result.logs)
            self.test_failures_since_last_success = 0
        else:
            print("*** Test failures detected. ***")
            self.test_failures_since_last_success += 1
            self.fix_test_failures(result.logs)

    def update_requirements_file(self, inputs):
        tool = UpdateRequirementsFileTool(directory="output/src", force=True)
        output = tool._run()
        print(output)

    def on_code_changed(self, inputs):
        self.update_requirements_file(inputs)
        self.run_tests(inputs)

    @agent
    def engineering_lead(self) -> Agent:
        return Agent(
            config=self.agents_config['engineering_lead'],
        )

    @agent
    def backend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['backend_engineer'],
            allow_code_execution=True,
            code_execution_mode="safe",  # Uses Docker for safety
            max_execution_time=120, 
            max_retry_limit=3,
            tools=[
                FileReadTool(),
                FileWriterTool(),
                RunTestsTool(),
                FileSearchTool(),
            ]
        )
    
    @agent
    def frontend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['frontend_engineer'],
            tools=[
                FileReadTool(),
                FileWriterTool(),
                RunTestsTool(),
                FileSearchTool(),
            ]
        )
    
    @agent
    def test_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['test_engineer'],
            allow_code_execution=True,
            code_execution_mode="safe",  # Uses Docker for safety
            tools=[
                FileReadTool(),
                FileWriterTool(),
                RunTestsTool(),
                FileSearchTool(),
            ]
        )
    
    @agent
    def streamlit_tester(self) -> Agent:
        return Agent(
            config=self.agents_config['streamlit_tester'],
            allow_code_execution=True,
            code_execution_mode="safe",  # Uses Docker for safety
            tools=[
                FileReadTool(),
                FileWriterTool(),
                RunTestsTool(),
                FileSearchTool(),
            ]
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
    def streamlit_test_task(self) -> Task:
        return Task(
            config=self.tasks_config['streamlit_test_task'],
        )
    
    @task
    def run_all_tests_task(self) -> Task:
        return Task(
            config=self.tasks_config['run_all_tests_task'],
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
            short_term_memory=short_term_memory,
            task_callback=self.on_code_changed,
            output_log_file="output/logs.txt",
        )