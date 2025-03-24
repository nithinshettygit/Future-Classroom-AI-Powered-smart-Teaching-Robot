import requests
from PIL import Image
from io import BytesIO

# API Credentials
API_KEY = "AIzaSyB8KDnZnqhfj5Ll1DOHksrcx_dMgeP-VaQ"  # Replace with your actual API key
CX = "c330687bc6e014984"  # Replace with your Custom Search Engine ID
search_query = "food digestion system"  # Modify as needed

# Fetch Image from Google Custom Search API
search_url = f"https://www.googleapis.com/customsearch/v1?q={search_query}&cx={CX}&key={API_KEY}&searchType=image&num=1"
search_response = requests.get(search_url)

if search_response.status_code == 200:
    data = search_response.json()
    if "items" in data and len(data["items"]) > 0:
        image_url = data["items"][0]["link"]
        
        # Fetch and Display the Image
        img_response = requests.get(image_url)
        if img_response.status_code == 200:
            img = Image.open(BytesIO(img_response.content))
            img.show()  # This will open the image in your default image viewer
        else:
            print("Failed to load image:", image_url)
    else:
        print("No image results found.")
else:
    print("Error:", search_response.status_code, search_response.text)