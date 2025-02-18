import os
from dotenv import load_dotenv
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.tasks import TaskOutput

from bot_flow.src.bot_flow.shared_utils.model_utils import get_model_identifier, get_model_api_key
from crewai_tools import SpiderTool
from bot_flow.src.bot_flow.types.types import SimpleSection

load_dotenv()
spider_tool = SpiderTool(
    custom_params={"depth": 2, "anti_bot": True, "proxy_enabled": True, "stealth": True},
    api_key=os.getenv("SPIDER_API_KEY"),
)

@CrewBase
class ScrapeCrew:
    """Scrape Crew"""

    def __init__(
        self,
        show_logs=False,
        directory="",
        idx=1,
        model_name: str = "4o-mini",
	):
        self.show_logs = show_logs
        self.directory = directory
        self.idx = idx
        self.model_name = model_name

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def web_scraper(self) -> Agent:
        return Agent(
            config=self.agents_config["web_scraper"],
            tools=[spider_tool],
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
    
    def save_web_content(self, task_output: TaskOutput):
        with open(f"{self.directory}/scraped/page_{self.idx}.md", "w") as file:
            # remove all rows that start with ``` to avoid conflicts with markdown
            task_output_raw = "\n".join([line for line in task_output.raw.split("\n") if not line.startswith("```")])
            file.write(task_output_raw)

    @task
    def web_scraping_task(self) -> Task:
        return Task(
            config=self.tasks_config['web_scraping_task'],
            agent=self.web_scraper(),
            max_retries=2,
            callback=self.save_web_content
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Search Crew"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=self.show_logs,
        )
