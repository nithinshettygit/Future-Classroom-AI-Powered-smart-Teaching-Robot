import json
import faiss
from sentence_transformers import SentenceTransformer

class ContentRetriever:
    def __init__(self, index_path, metadata_path, knowledgebase_path):
        """Initialize the retriever with FAISS index, metadata, and knowledge base."""
        self.index = faiss.read_index(index_path)
        with open(metadata_path, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)
        with open(knowledgebase_path, "r", encoding="utf-8") as f:
            self.knowledgebase = json.load(f)
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    def search(self, query, top_k=3):
        """Search for the most relevant content in the knowledge base."""
        query_embedding = self.model.encode([query], convert_to_numpy=True)
        distances, indices = self.index.search(query_embedding, top_k)

        results = []
        for i in range(len(indices[0])):
            idx = indices[0][i]
            results.append({
                "title": self.metadata[idx]["title"],
                "chapter": self.metadata[idx]["chapter"],
                "score": distances[0][i]
            })
        return results

    def is_in_syllabus(self, query):
        """Check if the query is related to the syllabus by searching the knowledge base."""
        # Convert the query to lowercase for case-insensitive matching
        query = query.lower()

        # Search for the query in the knowledge base
        for chapter, topics in self.knowledgebase.items():
            for topic, content in topics.items():
                if query in topic.lower() or query in content.lower():
                    return True  # Query is in syllabus
        return False  # Query is out of syllabus

    def get_explanation(self, query, top_k=1):
        """Retrieve the explanation for a given query."""
        # First, check if the query is in the syllabus
        if not self.is_in_syllabus(query):
            return None  # Indicates the query is out of syllabus

        # If the query is in the syllabus, retrieve the explanation
        results = self.search(query, top_k)
        if not results:
            return None  # No relevant information found

        best_match = results[0]
        best_title = best_match["title"]
        best_chapter = best_match["chapter"]

        if best_chapter in self.knowledgebase:
            for topic_title, topic_content in self.knowledgebase[best_chapter].items():
                if topic_title == best_title:
                    return topic_content
        return None  # Indicates the query is out of syllabus