#!./venv/bin/python3.12
import os
import time
import settings
from pathlib import Path
from logger import logger
from pydantic import BaseModel

from cf_client import CloudflareAPIClient


def main():

    # get current public server ip
    current_public_ip = _get_current_public_ip()
    logger.debug(f"public ip is '{current_public_ip}'")

    # check if previous public ip is stored in storage
    stored_ip = _get_stored_ip()
    logger.debug(f"stored ip is '{stored_ip}'")

    # if changed update dns record and update storage
    if stored_ip != current_public_ip.ip_addr:
        _store_ip(current_public_ip.ip_addr)

        cloudflare_client = CloudflareAPIClient(
                settings.API_TOKEN, 
                settings.ZONE_ID, 
                settings.DNS_ID
                )

        cloudflare_client.update_ip_address(current_public_ip.ip_addr)
    

class IfConfigResult(BaseModel):
    #model_config = ConfigDict(extra="ignore")
    ip_addr: str


def _get_current_public_ip() -> IfConfigResult:
    result_json = os.popen("curl -4 ifconfig.me/all.json").read()

    logger.debug(result_json)

    try:
        result: IfConfigResult = IfConfigResult.model_validate_json(result_json)
    except ValueError as ve:
        logger.error(f"Error in retrieving public ip, message: {ve}")
        result = IfConfigResult(ip_addr="")

    return result


def _get_stored_ip() -> str:
    path: Path = Path(settings.STORAGE_PATH)

    try:
        public_ip_address = path.read_text() 
    except FileNotFoundError:
        logger.debug("no previous ip was stored")
        return ""

    return public_ip_address


def _store_ip(ip: str):
    logger.debug(f"storing ip: {ip}")
    path = Path(settings.STORAGE_PATH)
    path.touch(exist_ok=True)

    with path.open("r+") as file:
        file.truncate(0)

    path.write_text(ip)


if __name__ == "__main__":
    while True:
        main()
        time.sleep(settings.SLEEP_IN_SECONDS)
