from faiss import write_index
from PIL import Image
from tqdm import tqdm
import argparse
import clip
import faiss
import json
import numpy as np
import os
import torch
import requests
from io import BytesIO


def index_from_urls(json_path):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device)
    model.eval()

    with open(json_path, "r") as f:
        image_map = json.load(f)

    images = []
    ids = []

    for obj_id, url in tqdm(image_map.items(), desc="Downloading and processing images"):
        try:
            response = requests.get(url, timeout=5)
            image = Image.open(BytesIO(response.content)).convert("RGB")
            images.append(preprocess(image))
            ids.append(int(obj_id))
        except Exception as e:
            print(f"Failed to process {obj_id}: {e}")

    if not images:
        print("No valid images processed.")
        return

    image_input = torch.stack(images).to(device)

    with torch.no_grad():
        image_features = model.encode_image(image_input).float()
    image_features /= image_features.norm(dim=-1, keepdim=True)
    image_features = image_features.cpu().numpy()

    index = faiss.IndexIDMap(faiss.IndexFlatIP(image_features.shape[1]))
    index.add_with_ids(image_features, np.array(ids))
    os.makedirs("static", exist_ok=True)
    write_index(index, "static/index.faiss")

    print(f"Indexed {len(ids)} images.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--json_path", type=str, default="files/highlighted_met_images.json")
    args = parser.parse_args()
    index_from_urls(args.json_path)