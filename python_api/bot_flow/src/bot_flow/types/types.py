from typing import List
from pydantic import BaseModel

class SearchResult(BaseModel):
    title: str
    link: str

class SearchResults(BaseModel):
    search_results: List[SearchResult] = []

class SimpleSection(BaseModel):
    title: str
    description: str
    key_talking_points: str

class SimpleOutline(BaseModel):
    sections: List[SimpleSection] = []

class OutlineCritique(BaseModel):
    valid: bool
    feedback: str
    improvements: List[str] = []

class SectionWordCount(BaseModel):
    title: str
    proposed_word_count: int

class WordCountDistribution(BaseModel):
    sections: List[SectionWordCount] = []

class FullSection(BaseModel):
    title: str
    description: str
    key_talking_points: str
    proposed_word_count: int

class FullOutline(BaseModel):
    sections: List[FullSection] = []

class TitleDescription(BaseModel):
    title: str
    description: str
