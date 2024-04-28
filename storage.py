from pydantic import BaseModel
from pathlib import Path
from typing import List


class Domain(BaseModel):
    name: str
    is_active: bool
    ip_address: str
    type: str
    proxied: bool


class Storage(BaseModel):
    domains: List[Domain]


def save(storage: Storage):
    path = Path("storage.json")
    path.touch(exist_ok=True)
    path.write_text(storage.model_dump_json())



