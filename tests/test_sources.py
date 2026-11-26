"""检查合成资料可读取且不改写原记录。"""

from pathlib import Path
import tempfile
import unittest

from read_sources import inventory, observations


class SourceTests(unittest.TestCase):
    source = Path(__file__).resolve().parents[1] / "examples"

    def test_inventory(self):
        self.assertEqual(sorted(inventory(self.source)), ['assigned', 'members', 'partitions', 'retention_seconds'])

    def test_observations(self):
        first = list(observations(self.source / "shift.jsonl"))
        second = list(observations(self.source / "contrast.jsonl"))
        self.assertEqual((len(first), len(second)), (12, 5))
        self.assertNotEqual(first, second)

    def test_invalid_order(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "order.jsonl"
            path.write_text('{"at":3,"kind":"request"}\n{"at":2,"kind":"receipt"}\n', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "order.jsonl:2"):
                list(observations(path))
