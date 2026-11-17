import json
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from agentic_eval.core_evals.llm_services import fi_api_service as service


def test_usage_logging_returns_when_server_stalls(monkeypatch):
    release = threading.Event()
    received = []

    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            received.append(
                json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            )
            if not release.wait(4):
                self.send_response(204)
                self.end_headers()

        def log_message(self, *args):
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    monkeypatch.setattr(
        service, "API_BASE_URL", f"http://127.0.0.1:{server.server_port}"
    )
    monkeypatch.setattr(service.FiApiKey, "_fi_api_key", "test-key")
    try:
        started = time.monotonic()
        result = service.FiApiService.log_usage("accuracy", "batch")
        elapsed = time.monotonic() - started
    finally:
        release.set()
        server.shutdown()
        server.server_close()
        worker.join(timeout=1)
    assert result is None
    assert received[0]["evalName"] == "accuracy"
    assert elapsed < 3, f"Optional usage logging blocked for {elapsed:.2f}s"
