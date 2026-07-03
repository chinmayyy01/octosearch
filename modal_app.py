import modal

app = modal.App("octosearch")

image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install_from_requirements("backend/requirements.txt")
    .run_commands(
        "python -c 'from sentence_transformers import SentenceTransformer; SentenceTransformer(\"all-MiniLM-L6-v2\")'"
    )
    .add_local_dir("backend", remote_path="/root/backend")
)

@app.function(
    image=image,
    min_containers=1,
    timeout=900,
    secrets=[modal.Secret.from_name("octosearch-secrets")],
)
@modal.concurrent(max_inputs=20)
@modal.asgi_app()
def fastapi_app():
    import sys
    sys.path.insert(0, "/root/backend")
    from backend.api import app as web_app
    return web_app