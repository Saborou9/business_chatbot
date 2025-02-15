import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from pydantic import BaseModel, Field

from src.bot_flow.shared_utils.model_utils import get_model_identifier, get_model_api_key

# Define a Pydantic model for the expected output
class InputProcessingOutput(BaseModel):
    intent_classification: str = Field(..., description="One of 'market_research', 'business_knowledge', or 'legal'")
    refined_question: str = Field(..., description="A clear, concise version of the original question")
    intent_confidence_percentage: int = Field(..., ge=0, le=100, description="Confidence score from 0-100")
    clarification_request_if_needed: str = Field(default="", description="Any clarification needed")

@CrewBase
class InputProcessingCrew:
    """Input Processing Crew"""

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
            cache=False,
            output_format=InputProcessingOutput  # Specify the output format
        )

    @task
    def process_input_task(self) -> Task:
        return Task(
            description="""
            Analyze the user's input and classify its intent.
            
            REQUIRED OUTPUT:
            1. intent_classification: MUST be one of:
               - "market_research"
               - "business_knowledge"
               - "legal"
            2. refined_question: A clear, concise version of the original question
            3. intent_confidence_percentage: A numerical confidence score (0-100)
            4. clarification_request_if_needed: Any needed clarification (or empty string)
            
            Carefully analyze the input question, determine the primary intent, 
            refine the question for clarity, and provide a confidence score.
            """,
            agent=self.input_processing_agent(),
            expected_output=InputProcessingOutput,  # Use the Pydantic model
            output_json=InputProcessingOutput  # Use the Pydantic model
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Input Processing Crew"""
        return Crew(
            agents=[self.input_processing_agent()],
            tasks=[self.process_input_task()],
            process=Process.sequential,
            verbose=self.show_logs,
        )
