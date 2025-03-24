from flask import Flask, request, jsonify, render_template
from retrieval import ContentRetriever
from generation import ContentGenerator

app = Flask(__name__)

# Initialize retriever and generator
retriever = ContentRetriever(
    "data/textbook_faiss.index",
    "data/metadata.json"
)
generator = ContentGenerator()

@app.route("/")
def home():
    """Render the chat interface."""
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    """Handle user queries and return the generated response."""
    try:
        # Get the user's query from the request
        data = request.json
        query = data.get("query")

        if not query:
            return jsonify({"error": "No query provided"}), 400

        # Retrieve explanation
        explanation = retriever.get_explanation(query)

        # Generate detailed and student-friendly content
        prompt = f"Explain the concept of {query} based on the following information: {explanation}\n\n"
        generated_explanation = generator.generate_content(prompt)

        # Return the response
        return jsonify({
            "query": query,
            "response": generated_explanation
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
