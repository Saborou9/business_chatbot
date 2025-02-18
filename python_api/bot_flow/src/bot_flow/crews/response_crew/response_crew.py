import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

from bot_flow.src.bot_flow.types.types import ResponseOutput
from bot_flow.src.bot_flow.shared_utils.model_utils import get_model_identifier, get_model_api_key

@CrewBase
class ResponseCrew:
    """Poem Crew"""

    def __init__(
        self,
        show_logs=False,
        model_name="4o-mini",
        directory="",
        inputs = None
    ):
        self.show_logs = show_logs
        self.model_name = model_name
        self.directory = directory
        self.inputs = inputs or {}

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def final_response_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["final_response_agent"],
            llm=LLM(
                model=get_model_identifier(self.model_name),
                api_key=os.getenv(get_model_api_key(self.model_name)),
                max_tokens=8192,
                temperature=0.1,
                top_p=0.65,
                presence_penalty=0.1,
                frequency_penalty=0.4,
            ),
            verbose=self.show_logs,
            cache=False
        )

    @task
    def finalize_response_task(self) -> Task:
        return Task(
            config=self.tasks_config["finalize_response"],
            agent=self.final_response_agent(),
            output_pydantic=ResponseOutput
            context=self.inputs
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Research Crew"""
        
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
