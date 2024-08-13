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




