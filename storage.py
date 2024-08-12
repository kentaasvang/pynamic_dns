from pydantic import BaseModel
from pathlib import Path
from typing import List
import logging
import settings

class DNSRecord(BaseModel):
    id: str
    name: str
    domain: str 
    update_ip_address: bool = False
    ip_address: str
    type: str
    proxied: bool


class Storage(BaseModel):
    dns_records: List[DNSRecord]


def save(storage: Storage):
    logging.debug("saving storage")
    path = Path("storage.json")
    path.touch(exist_ok=True)

    if settings.DEBUG:
        path.write_text(storage.model_dump_json(indent=4))
    else:
        path.write_text(storage.model_dump_json())


def read() -> Storage:
    logging.debug("Reading storage")
    path = Path("storage.json")
    content = path.read_text()
    try:
        storage = Storage.model_validate_json(content)
        return storage
    except ValueError as ve:
        logging.error("Failed to parse storage.sjon - %s" % ve)
        exit("Failed to parse storage.sjon - %s" % ve)



