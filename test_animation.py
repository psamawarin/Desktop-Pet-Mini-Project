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

            with self.assertRaisesRegex(FileNotFoundError, r"bored_3\.svg"):
                frame_paths(asset_dir, "bored")

    def test_png_frames_are_supported(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            asset_dir = Path(temporary_directory)
            for frame_number in range(1, 5):
                (asset_dir / f"walking_left_{frame_number}.png").touch()

            paths = frame_paths(asset_dir, "walking_left")

            self.assertEqual(len(paths), 4)
            self.assertTrue(all(path.suffix == ".png" for path in paths))

    def test_click_and_hover_frames_are_supported(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            asset_dir = Path(temporary_directory)
            for animation_name in ("click", "hover"):
                for frame_number in range(1, 5):
                    (asset_dir / f"{animation_name}_{frame_number}.png").touch()

            self.assertEqual(len(frame_paths(asset_dir, "click")), 4)
            self.assertEqual(len(frame_paths(asset_dir, "hover")), 4)

    def test_unknown_animation_set_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            with self.assertRaisesRegex(ValueError, "Unknown animation set"):
                frame_paths(Path(temporary_directory), "walking_right") # mirror walking left at run time


if __name__ == "__main__":
    unittest.main()