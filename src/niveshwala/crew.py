from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai_tools import SerperDevTool
from niveshwala.tools.custom_tool import MyCustomTool
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class NiveshWala():
    """NiveshWala crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'], # type: ignore[index]
            verbose=True,
            tools=[SerperDevTool(), MyCustomTool()]
        )
    
    @agent
    def analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['analyst'],
            verbose=True,
            tools=[SerperDevTool(), MyCustomTool()]
        )

    @agent
    def advisor(self) -> Agent:
        return Agent(
            config=self.agents_config['advisor'],
            verbose=True,
            tools=[SerperDevTool(), MyCustomTool()]
        )
    
    @agent
    def risk_manager(self) -> Agent:
        return Agent(
            config=self.agents_config['risk_manager'],
            verbose=True,
            tools=[SerperDevTool(), MyCustomTool()]
        )

    @agent
    def trend_predictor(self) -> Agent:
        return Agent(
            config=self.agents_config['trend_predictor'],
            verbose=True,
            tools=[SerperDevTool(), MyCustomTool()]
        )

    @agent
    def educator(self) -> Agent:
        return Agent(
            config=self.agents_config['educator'],
            verbose=True,
            tools=[SerperDevTool()]
        )

    @agent
    def compliance_officer(self) -> Agent:
        return Agent(
            config=self.agents_config['compliance_officer'],
            verbose=True,
            tools=[SerperDevTool()]
        )

    @agent
    def reporter(self) -> Agent:
        return Agent(
            config=self.agents_config['reporter'], # type: ignore[index]
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'], # type: ignore[index]
        )
    
    @task
    def analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['analysis_task'],  # type: ignore[index]
        )

    @task
    def advisory_task(self) -> Task:
        return Task(
            config=self.tasks_config['advisory_task'],  # type: ignore[index]
        )

    @task
    def risk_evaluation_task(self) -> Task:
        return Task(
            config=self.tasks_config['risk_evaluation_task'],  # type: ignore[index]
        )

    @task
    def trend_forecasting_task(self) -> Task:
        return Task(
            config=self.tasks_config['trend_forecasting_task'],  # type: ignore[index]
        )

    @task
    def educator_task(self) -> Task:
        return Task(
            config=self.tasks_config['educator_task'],  # type: ignore[index]
        )

    @task
    def compliance_task(self) -> Task:
        return Task(
            config=self.tasks_config['compliance_task'],  # type: ignore[index]
        )

    @task
    def report_task(self) -> Task:
        return Task(
            config=self.tasks_config['report_task'], # type: ignore[index]
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the NiveshWala crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
 