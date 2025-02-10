import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

from src.bot_flow.shared_utils.model_utils import get_model_identifier, get_model_api_key

@CrewBase
class LegalCrew:
    """Poem Crew"""

    def __init__(
        self,
        show_logs=False,
        model_name="4o-mini",
        directory="",
    ):
        self.show_logs = show_logs
        self.model_name = model_name
        self.directory = directory

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def legal_compliance_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["legal_compliance_agent"],
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
    def provide_legal_guidance_task(self) -> Task:
        return Task(
            config=self.tasks_config["provide_legal_guidance"],
            agent=self.legal_compliance_agent()
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
