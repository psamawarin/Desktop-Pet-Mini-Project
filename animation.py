from pathlib import Path

FRAME_COUNT = 4
ANIMATION_NAMES = ("idle", "walking_left", "bored")
FRAME_EXTENSIONS = (".svg", ".png")


def frame_paths(
    asset_dir: Path,
    animation_name: str,
) -> list[Path]:
    if animation_name not in ANIMATION_NAMES:
        raise ValueError(f"Unknown animation set: {animation_name}")

    paths = []
    missing = []
    for frame_number in range(1, FRAME_COUNT + 1):
        frame_stem = f"{animation_name}_{frame_number}"
        candidates = [asset_dir / f"{frame_stem}{extension}" for extension in FRAME_EXTENSIONS]
        frame_path = next((path for path in candidates if path.is_file()), None)
        if frame_path is None:
            missing.append(" or ".join(path.name for path in candidates))
        else:
            paths.append(frame_path)
    if missing:
        missing_names = ", ".join(missing)
        raise FileNotFoundError(
            f"Animation set '{animation_name}' is incomplete; missing: {missing_names}"
        )
    return paths
