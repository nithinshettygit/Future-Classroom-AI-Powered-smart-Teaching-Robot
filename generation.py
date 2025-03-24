import ollama
import requests
from PIL import Image
from io import BytesIO
import os
import re  # For sanitizing filenames

class ContentGenerator:
    def __init__(self, model_name="llama3.2"):
        """Initialize the Ollama-based LLaMA model."""
        self.model_name = model_name

    def generate_content(self, prompt, explanation):
        """Generate content using the Ollama LLaMA model."""
        try:
            # If the explanation is None, the topic is out of syllabus
            if explanation is None:
                enhanced_prompt = (
                    f"Explain the concept of '{prompt}' in detail for a 10th-grade student. "
                    "This is out of syllabus content, so provide a comprehensive explanation:\n\n"
                )
            else:
                enhanced_prompt = (
                    f"Explain the concept of '{prompt}' in detail for a 10th-grade student. "
                    f"Use the following information to guide your explanation: {explanation}\n\n"
                )

            # Use Ollama's generate API
            response = ollama.generate(
                model=self.model_name,
                prompt=enhanced_prompt,
                options={
                    "num_predict": 600,  # Control response length
                    "temperature": 0.7,  # Balance creativity and accuracy
                    "top_p": 0.9,        # Control diversity of responses
                    "repeat_penalty": 1.1 # Reduce repetition
                }
            )
            return response["response"]
        except Exception as e:
            print(f"Error generating content: {e}")
            return "Failed to generate content."

    def sanitize_filename(self, query):
        """Sanitize the query to create a valid filename."""
        # Remove special characters and replace spaces with underscores
        sanitized = re.sub(r'[^\w\s-]', '', query)  # Remove invalid characters
        sanitized = sanitized.replace(' ', '_')      # Replace spaces with underscores
        return sanitized.lower()  # Convert to lowercase for consistency

    def fetch_image(self, query):
        """Fetch an image using Google Custom Search API."""
        API_KEY = "AIzaSyB8KDnZnqhfj5Ll1DOHksrcx_dMgeP-VaQ"  # Replace with your actual API key
        CX = "c330687bc6e014984"  # Replace with your Custom Search Engine ID

        # Sanitize the query to create a valid filename
        sanitized_query = self.sanitize_filename(query)

        # Fetch Image from Google Custom Search API
        search_url = f"https://www.googleapis.com/customsearch/v1?q={query}&cx={CX}&key={API_KEY}&searchType=image&num=1"
        search_response = requests.get(search_url)

        if search_response.status_code == 200:
            data = search_response.json()
            if "items" in data and len(data["items"]) > 0:
                image_url = data["items"][0]["link"]
                
                # Fetch and Save the Image
                img_response = requests.get(image_url)
                if img_response.status_code == 200:
                    img = Image.open(BytesIO(img_response.content))
                    image_path = os.path.join("static", "images", f"{sanitized_query}.jpg")
                    img.save(image_path)  # Save the image to the static/images directory
                    return image_path  # Return the path to the saved image
                else:
                    print("Failed to load image:", image_url)
            else:
                print("No image results found.")
        else:
            print("Error:", search_response.status_code, search_response.text)
        return None

    def generate_image_description(self, image_path):
        """Generate a detailed description of the image using the Ollama model."""
        try:
            # Enhanced prompt for image description
            prompt = (
                "You are a friendly and knowledgeable teacher explaining an image to a 10th-grade student. "
                "Your goal is to make the explanation clear, engaging, and easy to understand. "
                "Describe the following image in detail:\n\n"
                f"Image: {image_path}\n\n"
            )

            # Use Ollama's generate API
            response = ollama.generate(
                model=self.model_name,
                prompt=prompt,
                options={
                    "num_predict": 200,  # Control response length
                    "temperature": 0.7,  # Balance creativity and accuracy
                    "top_p": 0.9,        # Control diversity of responses
                    "repeat_penalty": 1.1 # Reduce repetition
                }
            )
            return response["response"]
        except Exception as e:
            print(f"Error generating image description: {e}")
            return "Failed to generate image description."