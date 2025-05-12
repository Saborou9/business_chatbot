#!/usr/bin/env python
import os
from datetime import datetime
from typing import List
from random import randint
from pydantic import BaseModel
from crewai.flow.flow import Flow, listen, start, router, or_

from bot_flow.src.bot_flow.types.types import SearchResult, InputProcessingOutput, SearchOutput, BusinessKnowledgeOutput, LegalOutput, FactCheckingOutput, ResponseOutput
from bot_flow.src.bot_flow.shared_utils.flow_utils import FlowUtils

from bot_flow.src.bot_flow.crews.input_processing_crew.input_processing_crew import InputProcessingCrew
from bot_flow.src.bot_flow.crews.business_knowledge_crew.business_knowledge_crew import BusinessKnowledgeCrew
from bot_flow.src.bot_flow.crews.fact_checking_crew.fact_checking_crew import FactCheckingCrew
from bot_flow.src.bot_flow.crews.legal_crew.legal_crew import LegalCrew
from bot_flow.src.bot_flow.crews.response_crew.response_crew import ResponseCrew
from bot_flow.src.bot_flow.crews.scrape_crew.scrape_crew import ScrapeCrew
from bot_flow.src.bot_flow.crews.search_crew.search_crew import SearchCrew


class BuddyState(BaseModel):
    question: str = ""
    input_details: InputProcessingOutput = InputProcessingOutput()
    search_results: SearchOutput = SearchOutput()
    search_results_links: SearchOutput = SearchOutput()
    parsed_webpages: List[str] = []
    business_knowledge: BusinessKnowledgeOutput = BusinessKnowledgeOutput()
    legal_analysis: LegalOutput = LegalOutput()
    fact_checked_info: FactCheckingOutput = FactCheckingOutput()
    response: ResponseOutput = ResponseOutput()
    is_processing: bool = False


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
        super().__init__()
        self.question = question
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
        self.state.question = self.question

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

    @router(process_input)
    def route_to_crew(self):
        print(f"Routing based on intent: {self.state.input_details.intent_classification}")
        intent = self.state.input_details.intent_classification
        
        if intent == "market_research":
            print("Routing to search_google")
            return "search_google_intent"
        elif intent == 'business_knowledge':
            print("Routing to business_knowledge")
            return "business_knowledge_intent"
        elif intent == 'legal':
            print("Routing to legal")
            return "legal_intent"
        else:
            print("No clear intent detected. Defaulting to search.")

    @listen("search_google_intent")
    def search_google(self):
        print("Searching Google")
        result = (
            SearchCrew(
                show_logs=self.show_logs,
                search_timeframe=self.search_timeframe,
                search_results=self.search_results,
                model_name=self.model_name,
                topic=self.state.question,
                search_results_parsed=self.search_results_parsed
            )
            .crew()
            .kickoff(inputs={
                "current_date": self.current_date,
                "topic": self.state.question,
                "search_results_parsed": self.search_results_parsed
            })
        )
        
        # Add error checking
        if result and result.pydantic:
            self.state.search_results_links = result.pydantic
            self.utils.save_step_result_to_file(self.directory, "search_google", self.state.search_results_links, format="pydantic")
        else:
            print("Error: Search crew returned no results")
            # Optionally, set a default or handle the error
            self.state.search_results_links = SearchOutput()

    @listen(search_google)
    def parse_results(self):
        print("Parsing results")
        
        # # Only for testing
        # # read webpage links from file save during searching
        # with open(f"{self.directory}/search_google.json", "r") as f:
        #     datax = json.load(f)
        #     self.state.search_results_links = SearchResults(**datax)
        
        inputs_array = [{"topic": self.state.input_details.refined_question, "url": link.link} for link in self.state.search_results_links.search_results]

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
                self.state.parsed_webpages.append(kb_article)

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
                "question": self.state.input_details.refined_question,
            })
        )
        self.state.business_knowledge = result.pydantic
        self.utils.save_step_result_to_file(self.directory, "business_knowledge", self.state.business_knowledge, format="pydantic")


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
                "question": self.state.input_details.refined_question,
            })
        )
        self.state.legal_analysis = result.pydantic
        self.utils.save_step_result_to_file(self.directory, "legal", self.state.legal_analysis, format="pydantic")

    @listen(or_(business_knowledge, legal))
    def fact_checking(self):
        print("Fact checking")

        inputs = {
            "question": self.question
        }

        intent = self.state.input_details.intent_classification

        if intent == "business_knowledge" and self.state.business_knowledge:
            inputs["business_knowledge"] = str(self.state.business_knowledge.dict())

        if intent == "legal" and self.state.legal_analysis:
            inputs["legal_analysis"] = str(self.state.legal_analysis.legal_analysis)

        result = (
            FactCheckingCrew(
                show_logs=self.show_logs,
                model_name=self.model_name
            )
            .crew()
            .kickoff(inputs=inputs)
        )
        self.state.fact_checked_info = result.pydantic
        self.utils.save_step_result_to_file(self.directory, "fact_checking", self.state.fact_checked_info, format="pydantic")

    @listen(or_(parse_results, business_knowledge, legal))
    def response(self):
        print("Generating response")
        self.state.is_processing = True
        
        try:
            # Prepare inputs dynamically based on available state
            inputs = {
                "question": self.question,
                "market_research": "",
                "search_results": "",
                "business_knowledge": "",
                "legal_analysis": "",
            }

            # Conditionally add inputs based on intent and available state
            intent = self.state.input_details.intent_classification

            if intent == "market_research" and self.state.search_results_links:
                inputs["search_results"] = "\n".join(
                    [f"- {result.title}: {result.link}" 
                     for result in self.state.search_results_links.search_results]
                )

            if intent == "business_knowledge" and self.state.business_knowledge:
                inputs["business_knowledge"] = str(self.state.business_knowledge)

            if intent == "legal" and self.state.legal_analysis:
                inputs["legal_analysis"] = str(self.state.legal_analysis.legal_analysis)

            # Kickoff the response crew with conditional inputs
            response_crew = (
                ResponseCrew(
                    show_logs=self.show_logs,
                    model_name=self.model_name
                )
            )

            response = response_crew.crew().kickoff(inputs=inputs)

            # Ensure we save the pydantic result
            if response and response.pydantic:
                self.utils.save_step_result_to_file(self.directory, "response", response.pydantic, format="pydantic")
                self.state.response = response.pydantic
                return self.state.response.final_response
            else:
                print("Error: Response crew returned no result")
                return "Unable to answer your question, try asking again..."
                
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return f"Error processing your request: {str(e)}"
            
        finally:
            self.state.is_processing = False

def kickoff():
    buddy_flow = BuddyFlow()
    buddy_flow.kickoff()

def plot():
    buddy_flow = BuddyFlow()
    buddy_flow.plot()

if __name__ == "__main__":
    kickoff()
