import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest

from agentic_eval.core.embeddings.serving_client import ModelServingClient


@pytest.mark.parametrize("text", ["one", ["one"], ["one", "second"]])
def test_infer_preserves_batch_vectors(text):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()

        def do_POST(self):
            body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            texts = body["text"] if isinstance(body["text"], list) else [body["text"]]
            vectors = [[len(value), 0.5] for value in texts]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps({"embeddings": vectors}).encode())

        def log_message(self, *args):
            pass

    server = HTTPServer(("127.0.0.1", 0), Handler)
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    client = ModelServingClient(f"http://127.0.0.1:{server.server_port}")
    try:
        expected = (
            [[len(value), 0.5] for value in text]
            if isinstance(text, list)
            else [3, 0.5]
        )
        assert client.get_embeddings(text, "openai", "test-model") == expected
    finally:
        client.close()
        server.shutdown()
        server.server_close()
