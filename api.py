import importlib.util
import os
import sys

# Render may run from repo root; ensure backend modules are importable.
BACKEND_DIR = os.path.join(os.path.dirname(__file__), "backend")
BACKEND_API_FILE = os.path.join(BACKEND_DIR, "api.py")

if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

spec = importlib.util.spec_from_file_location("octosearch_backend_api", BACKEND_API_FILE)
if spec is None or spec.loader is None:
    raise RuntimeError("Could not load backend/api.py")

module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

app = module.app
