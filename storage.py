import json
from pathlib import Path
from typing import Union


PathLike = Union[str, Path]
DEFAULT_NAME = "Pet"


def save_name(path: PathLike, name: str) -> None:
    clean_name = name.strip()
    if not clean_name:
        raise ValueError("Pet name cannot be empty")

    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(
        json.dumps({"name": clean_name}, indent=2),
        encoding="utf-8",
    )


def load_name(path: PathLike, default: str = DEFAULT_NAME) -> str:
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default

    name = data.get("name") if isinstance(data, dict) else None
    return name.strip() if isinstance(name, str) and name.strip() else default