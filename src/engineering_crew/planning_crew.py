from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff
from .memory import long_term_memory, short_term_memory, entity_memory
from .models.design import Design
from .models.backlog import Backlog
import os
import shutil

@CrewBase
class PlanningTeam():
    """EngineeringTeam crew"""

    agents_config = 'config/planning_agents.yaml'
    tasks_config = 'config/planning_tasks.yaml'

    @before_kickoff
    def purge_output_dir(self, inputs):
        # Delete the output directory if it exists
        shutil.rmtree('output', ignore_errors=True)
        os.makedirs('output/src', exist_ok=True)

        return inputs

    @agent
    def engineering_lead(self) -> Agent:
        return Agent(
            config=self.agents_config['engineering_lead'],
        )

    @agent
    def engineering_planner(self) -> Agent:
        return Agent(
            config=self.agents_config['engineering_lead'],
        )

    @task
    def design_task(self) -> Task:
        return Task(
            config=self.tasks_config['design_task'],
            output_pydantic=Design
        )

    @task
    def planning_task(self) -> Task:
        return Task(
            config=self.tasks_config['planning_task'],
            output_pydantic=Backlog
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