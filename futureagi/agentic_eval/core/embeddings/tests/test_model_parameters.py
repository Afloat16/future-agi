import json
import threading
from concurrent.futures import ThreadPoolExecutor
from http.server import BaseHTTPRequestHandler, HTTPServer

from agentic_eval.core.embeddings.serving_client import ModelServingClient


def test_concurrent_requests_do_not_mutate_shared_model_params(monkeypatch):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()

        def do_POST(self):
            body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            vector = [len(body["model_params"]["model"])]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps({"embeddings": [vector]}).encode())

        def log_message(self, *args):
            pass

    server = HTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    client = ModelServingClient(f"http://127.0.0.1:{server.server_port}")
    barrier = threading.Barrier(2)
    post = client.session.post

    def simultaneous_post(*args, **kwargs):
        barrier.wait(timeout=5)
        return post(*args, **kwargs)

    monkeypatch.setattr(client.session, "post", simultaneous_post)
    params = {"model": "configured"}

    def request(model):
        return client.get_embeddings("text", "openai", model, params)

    try:
        with ThreadPoolExecutor(max_workers=2) as pool:
            assert list(pool.map(request, ["a", "bb"])) == [[1], [2]]
        assert params == {"model": "configured"}
    finally:
        client.close()
        server.shutdown()
        server.server_close()
