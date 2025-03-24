from flask import Flask, request, jsonify, render_template
from retrieval import ContentRetriever
from generation import ContentGenerator
import os
import re  # For detecting topic changes

app = Flask(__name__)

# Initialize retriever and generator
retriever = ContentRetriever(
    "data/textbook_faiss.index",
    "data/metadata.json",
    "data/knowledgebase.json"  # Path to knowledgebase.json
)
generator = ContentGenerator()

# Store conversation history in memory (for simplicity)
conversation_history = []

def is_topic_change(query):
    """Detect if the user wants to change the topic."""
    # Keywords indicating a topic change
    topic_change_keywords = [
        "move to", "new topic", "new chapter", "let's discuss", "next topic", "next chapter"
    ]
    # Check if any keyword is in the query
    return any(keyword in query.lower() for keyword in topic_change_keywords)

@app.route("/")
def home():
    """Render the chat interface."""
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    """Handle user queries and return the generated response."""
    global conversation_history

    try:
        data = request.json
        query = data.get("query")

        if not query:
            return jsonify({"error": "No query provided"}), 400

        # Check if the user wants to change the topic
        if is_topic_change(query):
            conversation_history = []  # Reset conversation history
            return jsonify({
                "query": query,
                "response": "Sure! Let's move to a new topic. What would you like to discuss next?",
                "image": None,
                "image_description": ""
            })

        # Add the user's query to the conversation history
        conversation_history.append({"role": "user", "content": query})

        # Retrieve explanation
        explanation = retriever.get_explanation(query)

        # Generate detailed and student-friendly content
        generated_explanation = generator.generate_content(query, explanation)

        # If the explanation is None, the topic is out of syllabus
        if explanation is None:
            generated_explanation = (
                "This is out of syllabus content, but here's a detailed explanation:\n\n"
                + generated_explanation
            )

        # Fetch relevant image (handle errors gracefully)
        image_path = None
        if explanation is not None:  # Only fetch images for in-syllabus topics
            try:
                image_path = generator.fetch_image(query)
            except Exception as e:
                print(f"Error fetching image: {e}")

        # Generate image description (if image is available)
        image_description = ""
        if image_path:
            try:
                image_description = generator.generate_image_description(image_path)
                if not image_description:
                    image_description = "No description available for the image."
                # Ensure the image path is relative to the static folder
                image_path = image_path.replace("static/", "")
            except Exception as e:
                print(f"Error generating image description: {e}")

        # Add the model's response to the conversation history
        conversation_history.append({"role": "assistant", "content": generated_explanation})

        # Return the response with multimedia links
        return jsonify({
            "query": query,
            "response": generated_explanation,
            "image": image_path,  # Path to the fetched image (or None if failed)
            "image_description": image_description  # Description of the image (or empty if failed)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Create the static/images directory if it doesn't exist
    os.makedirs(os.path.join("static", "images"), exist_ok=True)
    app.run(debug=True)