import os
import subprocess
import sys

import pytest


@pytest.mark.parametrize("encoding", ["utf-8", "utf-8-sig", "utf-16", "utf-32"])
def test_json_dataset_encoding_is_independent_of_locale(tmp_path, encoding):
    path = tmp_path / "dataset.json"
    path.write_text('[{"text": "你好"}]', encoding=encoding)
    code = (
        "import sys\n"
        "from agentic_eval.core_evals.fi_loaders.text_loader import TextLoader\n"
        "data = TextLoader().load_json(sys.argv[1])\n"
        "assert data == [{'text': '\\u4f60\\u597d'}]\n"
    )
    env = os.environ | {
        "LC_ALL": "C",
        "PYTHONUTF8": "0",
        "PYTHONCOERCECLOCALE": "0",
    }
    result = subprocess.run(
        [sys.executable, "-c", code, str(path)],
        env=env,
        capture_output=True,
        text=True,
        timeout=20,
    )
    assert result.returncode == 0, result.stderr
