#!/usr/bin/env python
import os
from datetime import datetime
from typing import List
from random import randint
from pydantic import BaseModel
from crewai.flow import Flow, listen, start, router, or_

from src.bot_flow.types.types import SearchResult, InputProcessingOutput, SearchOutput, BusinessKnowledgeOutput, LegalOutput, FactCheckingOutput, ResponseOutput
from src.bot_flow.shared_utils.flow_utils import FlowUtils

from src.bot_flow.crews.input_processing_crew.input_processing_crew import InputProcessingCrew
from src.bot_flow.crews.business_knowledge_crew.business_knowledge_crew import BusinessKnowledgeCrew
from src.bot_flow.crews.fact_checking_crew.fact_checking_crew import FactCheckingCrew
from src.bot_flow.crews.legal_crew.legal_crew import LegalCrew
from src.bot_flow.crews.response_crew.response_crew import ResponseCrew
from src.bot_flow.crews.scrape_crew.scrape_crew import ScrapeCrew
from src.bot_flow.crews.search_crew.search_crew import SearchCrew


class BuddyState(BaseModel):
    question: str = ""
    input_details: InputProcessingOutput = InputProcessingOutput(
        intent_classification='market_research',
        refined_question='',
        intent_confidence_percentage=50
    )
    search_results: SearchOutput = SearchOutput()
    business_knowledge: BusinessKnowledgeOutput = BusinessKnowledgeOutput()
    legal_analysis: LegalOutput = LegalOutput()
    fact_checked_info: FactCheckingOutput = FactCheckingOutput()
    response: ResponseOutput = ResponseOutput()


class BuddyFlow(Flow[BuddyState]):

    def __init__(
        self,
        question: str,
        show_logs: bool,
        directory: str,
        search_timeframe: str,
        search_results: int,
        search_results_parsed: int,
        model_name: str,
    ):
        # Initialize with the state
        super().__init__(state=BuddyState(question=question))
        
        self.show_logs = show_logs
        self.directory = (f"output/{directory}")
        self.search_timeframe = search_timeframe
        self.search_results = search_results
        self.search_results_parsed = search_results_parsed
        self.model_name = model_name
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        self.knowledge_collection_name = f"knowledge_default_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"

        self.utils = FlowUtils()

        # create output directory
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        
        # create scraped subdirectory in output directory
        if not os.path.exists(f"{self.directory}/scraped"):
            os.makedirs(f"{self.directory}/scraped")

    @start()
    def process_input(self):
        print("Processing users input")
        result = (
            InputProcessingCrew(
                show_logs=self.show_logs,
                model_name=self.model_name
            )
            .crew()
            .kickoff(inputs={
                'question': self.state.question
            })
        )
        
        # Add error handling and logging
        if result and result.pydantic:
            self.state.input_details = result.pydantic
            self.utils.save_step_result_to_file(self.directory, "process_input", self.state, format="pydantic")
        else:
            print("Error: Input processing crew returned no result")
            # Set a default intent to prevent NoneType error
            self.state.input_details = InputProcessingOutput(
                intent_classification='market_research',
                refined_question=self.state.question,
                intent_confidence_percentage=50
            )

    @router(process_input)
    def route_to_crew(self):
        intent = self.state.input_details.get('intent_classification', '')
        
        if intent == 'market_research':
            return self.search_google
        elif intent == 'business_knowledge':
            return self.business_knowledge
        elif intent == 'legal':
            return self.legal
        else:
            # Default fallback
            print("No clear intent detected. Defaulting to search.")
            return self.search_google

    @listen("search_google_intent")
    def search_google(self):
        print("Searching Google")
        result = (
            SearchCrew(
                show_logs=self.show_logs,
                search_timeframe=self.search_timeframe,
                search_results=self.search_results,
                model_name=self.model_name,
                topic=self.state.question,  # Pass the question as topic
                search_results_parsed=self.search_results_parsed
            )
            .crew()
            .kickoff(inputs={
                "current_date": self.current_date,
                "topic": self.state.question,
                "search_results_parsed": self.search_results_parsed
            })
        )
        self.state.search_results_links = result.pydantic
        self.utils.save_step_result_to_file(self.directory, "search_google", self.state.search_results_links, format="pydantic")

    @listen(search_google)
    def parse_results(self):
        print("Parsing results")
        
        # # Only for testing
        # # read webpage links from file save during searching
        # with open(f"{self.directory}/search_google.json", "r") as f:
        #     datax = json.load(f)
        #     self.state.search_results_links = SearchResults(**datax)
        
        inputs_array = [{"topic": self.state.input_details.get('refined_question', ''), "url": link.link, "word_count": self.word_count} for link in self.state.search_results_links.search_results]

        # Remove all files from scrped directory
        for file in os.listdir(f"{self.directory}/scraped"):
            os.remove(f"{self.directory}/scraped/{file}")

        input_idx = 1
        for inputs in inputs_array:
            result = (
                ScrapeCrew(
                    show_logs=self.show_logs,
                    directory=self.directory,
                    idx=input_idx,
                    model_name=self.model_name
                )
                .crew()
                .kickoff(inputs=inputs)
            )
            input_idx += 1

        # Load all webpages content into a state variable
        for file in os.listdir(f"{self.directory}/scraped"):
            with open(f"{self.directory}/scraped/{file}", "r") as f:
                kb_article = f.read()
                self.embedding_tokens += len(self.encoding.encode(kb_article))
                self.state.parsed_webpages.append(kb_article)

        self.utils.save_step_result_to_file(self.directory, "parse_results", self.state.raw_outlines, format="pydantic")

    @listen("business_knowledge_intent")
    def business_knowledge(self):
        print("Extracting business knowledge")
        result = (
            BusinessKnowledgeCrew(
                show_logs=self.show_logs,
                model_name=self.model_name
            )
            .crew()
            .kickoff(inputs={
                "raw_outlines": self.state.raw_outlines
            })
        )
        self.state.full_outlines = result.pydantic
        self.utils.save_step_result_to_file(self.directory, "business_knowledge", self.state.full_outlines, format="pydantic")


    @listen("legal_intent")
    def legal(self):
        print("Legal")
        result = (
            LegalCrew(
                show_logs=self.show_logs,
                model_name=self.model_name
            )
            .crew()
            .kickoff(inputs={
                "full_outlines": self.state.full_outlines
            })
        )
        self.state.full_outlines = result.pydantic
        self.utils.save_step_result_to_file(self.directory, "legal", self.state.full_outlines, format="pydantic")

    @listen(or_(business_knowledge, legal))
    def fact_checking(self):
        print("Fact checking")
        result = (
            FactCheckingCrew(
                show_logs=self.show_logs,
                model_name=self.model_name
            )
            .crew()
            .kickoff(inputs={
                "full_outlines": self.state.full_outlines
            })
        )
        self.state.full_outlines = result.pydantic
        self.utils.save_step_result_to_file(self.directory, "fact_checking", self.state.full_outlines, format="pydantic")

    @listen(or_(parse_results, business_knowledge, legal))
    def response(self):
        print("Generating response")
        result = (
            ResponseCrew(
                show_logs=self.show_logs,
                model_name=self.model_name
            )
            .crew()
            .kickoff(inputs={
                "full_outlines": self.state.full_outlines
            })
        )
        self.state.response = result.pydantic
        self.utils.save_step_result_to_file(self.directory, "response", self.state.response, format="pydantic")

def kickoff():
    buddy_flow = BuddyFlow()
    buddy_flow.kickoff()

def plot():
    buddy_flow = BuddyFlow()
    buddy_flow.plot()

if __name__ == "__main__":
    kickoff()
