import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

from src.bot_flow.shared_utils.model_utils import get_model_identifier, get_model_api_key

@CrewBase
class InputProcessingCrew:
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
    def input_processing_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["input_processing_agent"],
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
    def process_input_task(self) -> Task:
        return Task(
            config=self.tasks_config["process_input"],
            agent=self.input_processing_agent(),
            output_json=True,
            expected_output={
                "intent_classification": str,
                "refined_question": str,
                "intent_confidence_percentage": int,
                "clarification_request_if_needed": str
            }
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
