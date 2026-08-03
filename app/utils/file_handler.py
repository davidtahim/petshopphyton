import json
from pathlib import Path
from typing import Union


def ensure_parent_dir(path: Union[str, Path]) -> Path:
    file_path = Path(path)

    if not file_path.is_absolute():
        project_root = Path(__file__).resolve().parents[2]
        file_path = project_root / file_path

    file_path.parent.mkdir(parents=True, exist_ok=True)
    return file_path


def read_json(path: Union[str, Path], default):
    file_path = ensure_parent_dir(path)
    if not file_path.exists():
        file_path.write_text(json.dumps(default, ensure_ascii=False, indent=2), encoding="utf-8")
        return default

    with file_path.open("r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return default


def write_json(path: Union[str, Path], data) -> None:
    file_path = ensure_parent_dir(path)
    with file_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
