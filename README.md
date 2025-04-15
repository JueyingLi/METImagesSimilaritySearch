# METImagesSimilaritySearch

A visual similarity search tool for artworks from the Metropolitan Museum of Art (The MET), powered by CLIP and FAISS. Users can find visually similar artworks by typing a description or uploading an image.

---

## 🔍 Features

- **Search by Text**: Describe an artwork and retrieve visually similar images.
- **Search by Image**: Upload an image to find artworks that look similar.
- **CLIP ViT-B/32**: Uses OpenAI's CLIP model to extract semantic image/text embeddings.
- **FAISS Indexing**: Efficient similarity search over MET's highlighted collection.
- **Flask App Interface**: Lightweight web UI for interaction.

---

## 🏛️ Dataset

- Based on the [Highlighted MET collection](https://metmuseum.github.io/#search)
- Indexed images are fetched from MET's public image URLs and saved in `highlighted_met_images.json`

---

## 🧠 Model & Indexing

- **Model**: CLIP (`ViT-B/32`)
- **Indexing**:
  - Preprocess images with CLIP
  - Normalize and index using FAISS (`IndexFlatIP`)
- Stored index: `static/index.faiss`

---

## 📁 Project Structure

```text
met-image-clip-faiss/
├── app.py                     # CLIP-based image/text search logic
│
├── helpers/
│   ├── get_img_from_web.py    # use MET api to generate artifact id and image link pair for highlight artifacts
│   └── sql_helper             # connect to PostgreSQL served on Supabase storing artifact data (TODO)
│
├── index.py                   # Builds FAISS index from MET image URLs using CLIP
├── serve.py                   # Flask web server handling text/image search routes
├── requirements.txt           # Python dependencies
├── README.md                  # Project overview and usage instructions. You are HERE!
│
├── static/
│   ├── index.faiss            # FAISS index of image embeddings
│   └── styles.css             # CSS styling for the web UI
│
├── templates/
│   └── index.html             # HTML template for the frontend UI
│
└── files/
    └── highlighted_met_images.json  # Mapping from MET object IDs to image URLs
```

---

## 🚀 Getting Started

### 1. Clone and setup environment

```bash
git clone git@github.com:JueyingLi/METImagesSimilaritySearch.git
cd METImagesSimilaritySearch
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Build FAISS Index
```bash
python index_highlighted.py
```

### 3. Run Flask App
```bash
python serve.py
```
Visit http://localhost:5000 to try it out!

## ✨ Future Improvements

Add filters (e.g. by time period, culture, medium)

Embed and index metadata with multi-modal RAG

Host live demo on HuggingFace Spaces or AWS
