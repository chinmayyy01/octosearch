from sentence_transformers import SentenceTransformer

model = None


def _get_model():
    global model
    if model is None:
        model = SentenceTransformer("all-MiniLM-L6-v2")
    return model

def get_embeddings(texts):
    return _get_model().encode(texts)