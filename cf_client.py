import requests

from datetime import datetime
from logger import logger

from pydantic import BaseModel
from typing import Dict, List, Any, Optional, Union


class CloudflareDNSRecord(BaseModel):
    content: str
    created_on: datetime 
    id: str
    locked: bool
    meta: Dict[str, bool]
    modified_on: datetime 
    name: str
    proxiable: bool
    proxied: bool
    tags: List[Any]
    ttl: int 
    type: str
    zone_id: str
    zone_name: str


class CloudflareResponse(BaseModel):
    errors: List[Any]
    messages: List[Any]
    result: Union[List[CloudflareDNSRecord], CloudflareDNSRecord]
    result_info: Optional[Dict[str, int]] = None
    success: bool


class UpdateDNSRecord(BaseModel):
    content: str
    name: str
    type: str
    comment: str
    proxied: bool


class CFClient:

    BASE_URL = "https://api.cloudflare.com/client/v4/"

    def __init__(self, auth_key, zone_id):
        logger.debug("Initializing CFClient")
        self.auth_key = auth_key
        self.zone_id = zone_id

    def get_dns_records(self) -> Union[List[CloudflareDNSRecord], None]:
        url = self.BASE_URL + "zones/" + self.zone_id + "/dns_records"
        params = {"type": "A"}
        response = requests.get(url, params=params, headers={"Authorization": "Bearer " + self.auth_key})
        cf_response = CloudflareResponse(**response.json())

        if response.status_code == requests.codes.ok and cf_response.success:
            return cf_response.result

        return None

    def update_ip_address(self, dns_record: CloudflareDNSRecord, new_ip) -> bool:
        url = self.BASE_URL + "zones/" + dns_record.zone_id + "/dns_records/" + dns_record.id

        update_record = UpdateDNSRecord(
            content=new_ip, 
            proxied=dns_record.proxied,
            name=dns_record.name, 
            type=dns_record.type, 
            comment=f"Updated by pynamic_dns on '{datetime.now().isoformat()}'"
            )

        response = requests.put(
            url, 
            headers={"Authorization": "Bearer " + self.auth_key}, 
            json=update_record.model_dump()
            )

        cf_response = CloudflareResponse(**response.json())

        if response.status_code == requests.codes.ok and cf_response.success:
            return True

        return False

