import json
from typing import Any, List

class FlowUtils:
    @staticmethod
    def save_step_result_to_file(directory: str, step_name: str, result: Any, format: str = "md") -> None:
        """Save step result to file in specified format"""
        if format == "json":
            with open(f"{directory}/{step_name}.json", "w") as f:
                f.write(json.dumps(result, indent=4))
        elif format == "md":
            with open(f"{directory}/{step_name}.md", "w") as f:
                f.write(result)
        elif format == "pydantic":
            with open(f"{directory}/{step_name}.json", "w") as f:
                f.write(result.model_dump_json())

    @staticmethod
    def extract_last_speaker(text: str) -> str:
        """Extract the last speaker from the given text"""
        paragraphs = text.strip().split("\n\n")
        last_paragraph = paragraphs[-1] if len(paragraphs) >= 1 else text
        speaker = last_paragraph.split(":")[0]
        return speaker if speaker else ""

    @staticmethod
    def extract_first_speaker(text: str) -> str:
        """Extract the first speaker from the given text"""
        paragraphs = text.strip().split("\n\n")
        first_paragraph = paragraphs[0] if len(paragraphs) >= 1 else text
        speaker = first_paragraph.split(":")[0]
        return speaker if speaker else ""

    @staticmethod
    def split_into_chunks(content: str, max_chunk_size: int = 3000) -> List[str]:
        """
        Split content into chunks where each chunk contains full paragraphs
        and the size of the chunk does not exceed the maximum chunk size
        """
        paragraphs = content.split("\n\n")
        chunks = []
        current_chunk = []
        current_size = 0

        for paragraph in paragraphs:
            paragraph_size = len(paragraph)
            
            if current_size + paragraph_size > max_chunk_size:
                chunks.append("\n\n".join(current_chunk))
                current_chunk = []
                current_size = 0

            current_chunk.append(paragraph)
            current_size += paragraph_size + 2

        if current_chunk:
            chunks.append("\n\n".join(current_chunk))

        return chunks
