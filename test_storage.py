import tempfile
import unittest
from pathlib import Path

from storage import load_name, save_name


class StorageTests(unittest.TestCase):
    def test_save_and_load_name(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "pet.json"

            save_name(path, "  Biscuit  ")

            self.assertEqual(load_name(path), "Biscuit")

    def test_missing_file_uses_default_name(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "missing.json"

            self.assertEqual(load_name(path), "Pet")

    def test_invalid_json_uses_default_name(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "pet.json"
            path.write_text("not json", encoding="utf-8")

            self.assertEqual(load_name(path), "Pet")

    def test_empty_name_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "pet.json"

            with self.assertRaises(ValueError):
                save_name(path, "   ")


if __name__ == "__main__":
    unittest.main()