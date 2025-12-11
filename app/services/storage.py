"""
Storage service for saving queries, outputs, citations, and scores.
"""
from datetime import datetime
import json

def save_query_output(project_id: str, query: str, output: str, citations: list, score: float):
    """
    Save user query, output text, citations, and retrieval score into project master file or DB.

    Args:
        project_id: Unique project identifier
        query: User's query text
        output: Generated response from LLM
        citations: List of source citations
        score: Relevance score for the retrieval
    """
    record = {
        "project_id": project_id,
        "timestamp": datetime.utcnow().isoformat(),
        "query": query,
        "output": output,
        "citations": citations,
        "score": score,
    }
    # TODO: save record in DB or file system
    print(f"Saved record for project {project_id}: {record}")

    # For now, append to a JSON file
    # Later this should be moved to a proper database
    try:
        with open(f"data/processed/{project_id}_queries.json", "a") as f:
            json.dump(record, f)
            f.write("\n")
    except Exception as e:
        print(f"Error saving query output: {e}")
