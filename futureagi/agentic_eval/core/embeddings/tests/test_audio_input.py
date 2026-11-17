import base64
import wave
from io import BytesIO

import numpy as np
import pytest

from agentic_eval.core.embeddings.serving_client import ModelServingClient


@pytest.mark.parametrize("dtype", [None, np.float32, np.float64])
@pytest.mark.parametrize(
    "samples,expected",
    [
        ([-1.5, -1, 0, 1, 1.5], [-32767, -32767, 0, 32767, 32767]),
        ([-1, -0.5, 0, 0.5, 1], [-32767, -16383, 0, 16383, 32767]),
    ],
)
def test_waveform_pcm_clips_without_wraparound(dtype, samples, expected):
    value = list(samples) if dtype is None else np.array(samples, dtype=dtype)
    client = ModelServingClient()
    try:
        uri = client._process_audio_input(value)
    finally:
        client.close()
    with wave.open(BytesIO(base64.b64decode(uri.split(",", 1)[1]))) as audio:
        assert audio.getnchannels() == 1
        assert audio.getframerate() == 16000
        assert audio.getnframes() == len(samples)
        pcm = np.frombuffer(audio.readframes(len(samples)), dtype="<i2")
    np.testing.assert_array_equal(pcm, expected)
    np.testing.assert_array_equal(value, samples)
