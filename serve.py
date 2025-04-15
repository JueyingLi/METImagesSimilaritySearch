from flask import Flask, request, render_template, jsonify
from app import App
from PIL import Image
import requests
from io import BytesIO

flask_app = Flask(__name__)
app = App()


@flask_app.route("/")
def index():
    return render_template("index.html")


@flask_app.route("/search_text", methods=["GET"])
def search_text():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Missing query"}), 400

    results = app.search_by_text(query, results=5)
    return jsonify({"results": results})


@flask_app.route("/search_image", methods=["POST"])
def search_image():
    image = None

    if "image_url" in request.form:
        url = request.form["image_url"]
        try:
            response = requests.get(url)
            image = Image.open(BytesIO(response.content)).convert("RGB")
        except Exception as e:
            return jsonify({"error": f"Failed to load image from URL: {str(e)}"}), 400

    elif "image_file" in request.files:
        image_file = request.files["image_file"]
        try:
            image = Image.open(image_file).convert("RGB")
        except Exception as e:
            return jsonify({"error": f"Failed to open uploaded image: {str(e)}"}), 400

    if image is None:
        return jsonify({"error": "No image provided"}), 400

    results = app.search_by_image(image, results=5)
    return jsonify({"results": results})


if __name__ == "__main__":
    flask_app.run(port=5000)