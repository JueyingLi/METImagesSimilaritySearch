import requests
import json

# Step 1: Get all highlighted object IDs
search_url = "https://collectionapi.metmuseum.org/public/collection/v1/search"
params = {
    "isHighlight": "true",
    "q": "*"
}

response = requests.get(search_url, params=params)
data = response.json()
object_ids = data.get("objectIDs", [])
# Step 2: For each ID, fetch the image URL
object_images = {}

for obj_id in object_ids:
    object_url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{obj_id}"
    obj_data = requests.get(object_url).json()
    image_url = obj_data.get("primaryImage") or obj_data.get("primaryImageSmall")
    if image_url:
        object_images[obj_id] = image_url

# Step 3: Save to JSON file
with open("../files/highlighted_met_images.json", "w") as f:
    json.dump(object_images, f, indent=2)

print(f"Saved {len(object_images)} image URLs to highlighted_met_images.json")