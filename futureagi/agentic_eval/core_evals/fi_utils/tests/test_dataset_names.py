from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from agentic_eval.core_evals.fi_utils import dataset_helper


def test_dataset_names_are_distinct_with_a_frozen_clock(monkeypatch):
    class FrozenClock:
        @staticmethod
        def now():
            return datetime(2026, 1, 2, 3, 4, 5)

    monkeypatch.setattr(dataset_helper, "datetime", FrozenClock)
    with ThreadPoolExecutor(max_workers=8) as executor:
        names = list(executor.map(lambda _: dataset_helper.generate_unique_dataset_name(), range(1000)))
    assert len(set(names)) == len(names)
    assert all(name.startswith("Dataset-2026-01-02-03-04-05-") for name in names)
    custom = dataset_helper.generate_unique_dataset_name("batch/", "_")
    assert custom.startswith("batch/2026_01_02_03_04_05_")
