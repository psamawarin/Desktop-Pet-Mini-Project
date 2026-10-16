import tempfile
import unittest
from pathlib import Path

from animation import frame_paths


class AnimationFrameTests(unittest.TestCase):
    def test_frame_paths_are_numbered_and_ordered(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            asset_dir = Path(temporary_directory)
            for frame_number in range(1, 5):
                (asset_dir / f"idle_{frame_number}.svg").touch()

            paths = frame_paths(asset_dir, "idle")

            self.assertEqual(
                [path.name for path in paths],
                [f"idle_{frame_number}.svg" for frame_number in range(1, 5)],
            )

    def test_incomplete_set_reports_missing_frames(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            asset_dir = Path(temporary_directory)
            for frame_number in (1, 2, 4):
                (asset_dir / f"bored_{frame_number}.svg").touch()

            with self.assertRaisesRegex(FileNotFoundError, "bored_3.svg"):
                frame_paths(asset_dir, "bored")

    def test_png_frames_are_supported(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            asset_dir = Path(temporary_directory)
            for frame_number in range(1, 5):
                (asset_dir / f"walking_left_{frame_number}.png").touch()

            paths = frame_paths(asset_dir, "walking_left")

            self.assertTrue(all(path.suffix == ".png" for path in paths))

    def test_svg_is_preferred_when_both_formats_exist(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            asset_dir = Path(temporary_directory)
            for frame_number in range(1, 5):
                (asset_dir / f"idle_{frame_number}.svg").touch()
                (asset_dir / f"idle_{frame_number}.png").touch()

            paths = frame_paths(asset_dir, "idle")

            self.assertTrue(all(path.suffix == ".svg" for path in paths))

    def test_unknown_animation_set_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            with self.assertRaisesRegex(ValueError, "Unknown animation set"):
                frame_paths(Path(temporary_directory), "walking_right")


if __name__ == "__main__":
    unittest.main()