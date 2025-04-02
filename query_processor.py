import numpy as np
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Tuple
from embedding_generator import EmbeddingGenerator
@dataclass
class QueryResult:
    topic_content: str
    relevant_figures: List[Dict]
    subchapter: str

class QueryProcessor:
    def __init__(self, topic_index, figure_index, topic_meta, figure_meta):
        self.topic_index = topic_index
        self.figure_index = figure_index
        self.topic_meta = topic_meta
        self.figure_meta = figure_meta
        self.embedder = EmbeddingGenerator()

    def process_query(self, query: str) -> QueryResult:
        # Embed query
        query_embedding = self.embedder.generate_embeddings([query])
        
        # Find most relevant topic
        _, topic_indices = self.topic_index.search(query_embedding.astype('float32'), 1)
        topic = self.topic_meta[topic_indices[0][0]]
        
        # Find figures from same subchapter
        figures = [fig for fig in self.figure_meta if fig['subchapter'] == topic['subchapter']]
        
        return QueryResult(
            topic_content=topic['content'],
            relevant_figures=figures,
            subchapter=topic['subchapter']
        )