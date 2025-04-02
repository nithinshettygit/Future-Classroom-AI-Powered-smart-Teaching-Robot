from flask import Flask, render_template, request
from pathlib import Path
from data_loader import DataLoader
from embedding_generator import EmbeddingGenerator
from query_processor import QueryProcessor
from content_generator import ContentGenerator
import faiss
import numpy as np
import os

app = Flask(__name__)

# Configuration
BASE_DIR = Path(__file__).parent
DATA_PATH = BASE_DIR / "integrated.json"
IMAGE_DIR = BASE_DIR / "static" / "images"
os.makedirs(IMAGE_DIR, exist_ok=True)

def init_system():
    print("⚗️ Chemistry Teacher System Initializing...")
    
    # Load data
    data = DataLoader.load_data(DATA_PATH)
    
    # Prepare embeddings
    embedder = EmbeddingGenerator()
    
    # Create topic index
    topic_texts, topic_meta = DataLoader.prepare_topic_data(data)
    topic_embeddings = embedder.generate_embeddings(topic_texts)
    topic_index = embedder.create_faiss_index(topic_embeddings)
    
    # Create figure index
    figure_texts, figure_meta = DataLoader.prepare_figure_data(data)
    figure_embeddings = embedder.generate_embeddings(figure_texts)
    figure_index = embedder.create_faiss_index(figure_embeddings)
    
    return {
        'processor': QueryProcessor(topic_index, figure_index, topic_meta, figure_meta),
        'generator': ContentGenerator()
    }

system = init_system()

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        query = request.form.get('query', '').strip()
        if query:
            # Process query
            query_result = system['processor'].process_query(query)
            
            # Generate explanations
            explanation = system['generator'].generate_topic_explanation(
                query_result.topic_content,
                query_result.subchapter
            )
            
            # Process figures with image verification
            figures = []
            for fig in query_result.relevant_figures:
                figure_data = system['generator'].generate_figure_explanation(fig)
                
                # Verify image exists
                if figure_data['path'] and not Path(figure_data['path'].lstrip('/')).exists():
                    figure_data['path'] = None
                figures.append(figure_data)
            
            result = {
                'query': query,
                'explanation': explanation,
                'figures': figures,
                'subchapter': query_result.subchapter
            }
    
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)