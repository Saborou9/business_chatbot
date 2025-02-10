import os

from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

from src.bot_flow.shared_utils.model_utils import get_model_identifier, get_model_api_key
from src.bot_flow.types.types import SearchResults
from src.bot_flow.tools.serper_dev_tool import SerperDevTool

@CrewBase
class SearchCrew:
    """Search Crew"""

    def __init__(
        self,
        show_logs=False,
        search_timeframe: str = "d",
        search_results: int = 10,
        model_name: str = "4o-mini",
	):
        self.show_logs = show_logs
        self.search_timeframe = search_timeframe
        self.search_results = search_results
        self.model_name = model_name

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def search_agent(self) -> Agent:
        search_tool = SerperDevTool(
            search_type="trending",
            tbs=self.search_timeframe,
            n_results=self.search_results,
        )
        return Agent(
            config=self.agents_config["search_agent"],
            tools=[search_tool],
            llm=LLM(
                model=get_model_identifier(self.model_name),
                api_key=os.getenv(get_model_api_key(self.model_name)),
                max_tokens=8192,
            ),
            verbose=self.show_logs,
            cache=False
        )

    @task
    def search_task(self) -> Task:
        return Task(
            config=self.tasks_config["search_task"],
            agent=self.search_agent(),
            output_pydantic=SearchResults
    )

    @crew
    def crew(self) -> Crew:
        """Creates the Search Crew"""

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=self.show_logs,
        )
