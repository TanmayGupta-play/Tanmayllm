import os
import glob
import requests
from pexels_api import API

from dotenv import load_dotenv
load_dotenv("project.env")
# Ensure images directory exists
IMAGE_DIR = "./images/"
os.makedirs(IMAGE_DIR, exist_ok=True)

def get_images(query, n):
    client = API('5JV9cVZRTr6VUv9pqbYDWvxlluf7DvAtm1B8xL7VJvVia9ULckKbnYfc')  # Initialize API with key
    try:
        client.search(query, results_per_page=n, page=1)  # Perform search
        response_data = client.json  # Get API response
        
        if "photos" not in response_data or not response_data["photos"]:
            print(f"No images found for query: {query}")
            return []
        
        filenames = []
        image_urls = []
        imagePath=[]
        for photo in response_data["photos"][:n]:
            try:
                image_url = photo["src"]["original"]
                image_name = os.path.basename(image_url)
                image_path = os.path.join(IMAGE_DIR, image_name)
                imagePath.append(image_path)
                # Print the image URL
                print(f"Image URL: {image_url}")
                image_urls.append(image_url)
                
                # Download image using requests
                response = requests.get(image_url, stream=True)
                if response.status_code == 200 and "image" in response.headers.get("Content-Type", ""):
                    with open(image_path, "wb") as file:
                        for chunk in response.iter_content(1024):
                            file.write(chunk)
                    print(f"Downloaded: {image_path}")
                    filenames.append(image_path)
                else:
                    print(f"Skipping {image_url} - Not a valid image")
            except Exception as e:
                print(f"Error downloading {image_url}: {e}")

        return imagePath
    except Exception as e:
        print(f"Error fetching images for query '{query}': {e}")
        return [], []

def empty_images():
    try:
        file_list = glob.glob(os.path.join(IMAGE_DIR, "*"))
        for file_path in file_list:
            os.remove(file_path)
        print("Image directory cleaned.")
    except Exception as e:
        print(f"Error cleaning image directory: {e}")
