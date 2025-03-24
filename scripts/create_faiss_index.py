import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Paths
metadata_path = "data/metadata.json"
index_path = "data/textbook_faiss.index"

# Load metadata
with open(metadata_path, "r", encoding="utf-8") as f:
    metadata = json.load(f)

# Initialize model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Encode all metadata titles
embeddings = model.encode([entry["title"] for entry in metadata], convert_to_numpy=True)

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Save FAISS index
faiss.write_index(index, index_path)
print("FAISS index successfully created!")
