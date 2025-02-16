from typing import List, Optional
from pydantic import BaseModel

class SimpleSection(BaseModel):
    title: str
    description: str
    key_talking_pints: str

class SearchResult(BaseModel):
    title: str
    link: str

class SearchOutput(BaseModel):
    search_results: List[SearchResult] = []

class InputProcessingOutput(BaseModel):
    intent_classification: str = ""
    refined_question: str = ""
    intent_confidence_percentage: int = 0
    clarification_request_if_needed: str = ""

class BusinessKnowledgeOutput(BaseModel):
    insights: str = ""

class LegalOutput(BaseModel):
    legal_analysis: str = ""

class FactCheckingOutput(BaseModel):
    verified_information: str = ""

class ResponseOutput(BaseModel):
    final_response: str = ""
