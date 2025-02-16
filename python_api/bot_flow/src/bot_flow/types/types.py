from typing import List
from pydantic import BaseModel

class SearchResult(BaseModel):
    title: str
    link: str

class SearchResults(BaseModel):
    search_results: List[SearchResult] = []

class InputProcessingOutput(BaseModel):
    intent_classification: str  # One of 'market_research', 'business_knowledge', or 'legal'
    refined_question: str
    intent_confidence_percentage: int  # 0-100
    clarification_request_if_needed: str = ""
