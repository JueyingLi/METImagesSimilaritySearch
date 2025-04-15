from faiss import read_index
from PIL import Image
import clip
import json
import torch
import requests
from io import BytesIO
import numpy as np
import os


class App:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)
        self.model.eval()

        self.index = read_index("static/index.faiss")
        print("Index size:", self.index.ntotal)
        print("Expected features dim:", self.index.d)
        with open("files/highlighted_met_images.json", "r") as f:
            self.image_map = json.load(f)

        # Store ids and a list of corresponding image urls
        self.ids = list(self.image_map.keys())
        self.urls = list(self.image_map.values())

    def encode_image(self, image: Image.Image):
        image_input = self.preprocess(image).unsqueeze(0).to(self.device)
        with torch.no_grad():
            image_features = self.model.encode_image(image_input).float()
        image_features /= image_features.norm(dim=-1, keepdim=True)
        return image_features.cpu().numpy()

    def encode_text(self, text: str):
        text_tokens = clip.tokenize([text]).to(self.device)
        with torch.no_grad():
            text_features = self.model.encode_text(text_tokens).float()
        text_features /= text_features.norm(dim=-1, keepdim=True)
        return text_features.cpu().numpy()

    def search_by_text(self, search_text, results=3):
        query = self.encode_text(search_text)
        print("Text feature shape:", query.shape)
        _, indices = self.index.search(query, results)
        return [self.image_map[str(i)] for i in indices[0] if str(i) in self.image_map]

    def search_by_image(self, image: Image.Image, results=3):
        image_input = self.preprocess(image).unsqueeze(0).to(self.device)
        with torch.no_grad():
            image_features = self.model.encode_image(image_input).float()
        image_features /= image_features.norm(dim=-1, keepdim=True)
        image_features = image_features.cpu().numpy()

        distances, indices = self.index.search(image_features, results)

        print("Top match scores:", distances[0])
        print("Top match indices:", indices[0])
        return [self.image_map[str(i)] for i in indices[0] if str(i) in self.image_map]

    def run(self):
        print("Type 'exit' to quit.")
        print("Type 'img <path_or_url>' to search by image.")
        while True:
            query = input("Search: ")
            if query == "exit":
                break
            elif query.startswith("img "):
                image_path = query[4:].strip()
                result = self.search_by_image(image_path, results=1)[0]
                print(f"Top match: {result}")
                Image.open(requests.get(result, stream=True).raw).show()
            else:
                result = self.search_by_text(query, results=1)[0]
                print(f"Top match: {result}")
                Image.open(requests.get(result, stream=True).raw).show()


if __name__ == "__main__":
    app = App()
    app.run()
