import requests
import settings
import CloudFlare

from datetime import datetime
from logger import logger

from pydantic import BaseModel
from typing import Dict, List, Any, Optional, Union


class CloudflareDNSRecord(BaseModel):
    id: str
    zone_id: str
    zone_name: str
    name: str
    type: str
    content: str
    proxiable: bool
    proxied: bool
    ttl: int 
    meta: Dict[str, bool]
    comment: str
    tags: List[Any]
    created_on: datetime 
    modified_on: datetime 


class CloudflareResponse(BaseModel):
    errors: List[Any]
    messages: List[Any]
    result: CloudflareDNSRecord
    result_info: Optional[Dict[str, int]] = None
    success: bool

    
# {'result': {'id': '3a0bec6d94588d4d46e13e9b36844aef', 'zone_id': '018dde8b571634e98935b75069c35547', 'zone_name': 'asvang-it.no', 'name': 'pynamic_dns.asvang-it.no', 'type': 'A', 'content': '123.123.123.123', 'proxiable': True, 'proxied': False, 'ttl': 1, 'meta': {'auto_added': False, 'managed_by_apps': False, 'managed_by_argo_tunnel': False}, 'comment': "Updated by pynamic_dns on '2024-08-12T22:31:13.151443'", 'tags': [], 'created_on': '2024-08-12T19:54:15.426113Z', 'modified_on': '2024-08-12T20:31:13.784478Z'}, 'success': True, 'errors': [], 'messages': []}


class UpdateDNSRecord(BaseModel):
    content: str
    name: str
    type: str
    comment: str


class CloudflareAPIClient:

    BASE_URL = "https://api.cloudflare.com/client/v4"

    def __init__(self, auth_key, zone_id, dns_id):
        logger.debug("Initializing CFClient")
        self.auth_key = auth_key
        self.zone_id = zone_id
        self.dns_id = dns_id
        self._client: CloudFlare.CloudFlare = CloudFlare.CloudFlare(
                debug=settings.DEBUG,
                token=settings.API_TOKEN
                )

    def update_ip_address(self, new_ip) -> bool:
        logger.debug("updating ip address on record in cloudflare")
        #url = self.BASE_URL + "zones/" + settings.ZONE_ID + "/dns_records/" + dns_record.id
        url = f"{self.BASE_URL}/zones/{self.zone_id}/dns_records/{self.dns_id}"

        update_record = UpdateDNSRecord(
            content=new_ip, 
            name="pynamic_dns",
            type="A",
            comment=f"Updated by pynamic_dns on '{datetime.now().isoformat()}'"
            )

        response = requests.put(
            url, 
            headers={"Authorization": "Bearer " + self.auth_key}, 
            json=update_record.model_dump()
            )

        logger.debug(response.json())

        cf_response = CloudflareResponse(**response.json())

        if response.status_code == requests.codes.ok and cf_response.success:
            logger.debug("updating on cloudflare was successfull")
            return True

        logger.debug("updating on cloudflare was unsuccessfull")
        return False


if __name__ == "__main__":
    import settings
    cf_client = CloudflareAPIClient(settings.API_TOKEN, settings.ZONE_ID, settings.DNS_ID)
    cf_client.update_ip_address("123.123.123.123")




