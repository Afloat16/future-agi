import base64
from io import BytesIO

import pytest
from PIL import Image

from agentic_eval.core.embeddings.serving_client import ModelServingClient


@pytest.mark.parametrize(
    "mode,color",
    [
        ("RGBA", (5, 80, 201, 42)),
        ("LA", (80, 42)),
        ("P", 1),
        ("RGB", (5, 80, 201)),
        ("L", 80),
    ],
)
def test_generated_images_preserve_pixels_and_alpha(mode, color):
    source = Image.new(mode, (3, 2), color)
    client = ModelServingClient()
    try:
        uri = client._process_image_input(source)
    finally:
        client.close()
    decoded = Image.open(BytesIO(base64.b64decode(uri.split(",", 1)[1])))
    assert decoded.size == source.size
    assert decoded.mode == source.mode
    assert decoded.tobytes() == source.tobytes()


def test_existing_image_format_is_preserved():
    buffer = BytesIO()
    Image.new("RGB", (3, 2), "blue").save(buffer, format="JPEG")
    source = Image.open(BytesIO(buffer.getvalue()))
    client = ModelServingClient()
    try:
        uri = client._process_image_input(source)
    finally:
        client.close()
    decoded = Image.open(BytesIO(base64.b64decode(uri.split(",", 1)[1])))
    assert uri.startswith("data:image/jpeg;base64,")
    assert decoded.size == source.size
