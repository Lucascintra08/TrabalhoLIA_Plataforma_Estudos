# src/services/file_store.py
import json
from pathlib import Path
from typing import Type, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def load_model(path: Path, model_cls: Type[T], default: T) -> T:
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
        return model_cls.model_validate(data)
    return default


def save_model(path: Path, model: BaseModel):
    path.write_text(
        model.model_dump_json(indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
