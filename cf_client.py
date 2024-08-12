import requests
import settings
import CloudFlare

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

    sync_ip_with_server: bool = False


class CloudflareResponse(BaseModel):
    errors: List[Any]
    messages: List[Any]
    result: Union[List[CloudflareDNSRecord], CloudflareDNSRecord, None]
    result_info: Optional[Dict[str, int]] = None
    success: bool


class UpdateDNSRecord(BaseModel):
    content: str
    name: str
    type: str
    comment: str
    proxied: bool

class CloudflareDomain(BaseModel):
    id: str
    name: str
    status: str
    paused: bool
    type: str
    development_mode: int
    name_servers: List[str]
    original_name_servers: List[str]
    original_registrar: str
    original_dnshost: Union[str, None]
    modified_on: datetime
    created_on: datetime
    activated_on: datetime
    meta: Dict[str, Any]
    owner: Dict[str, Any]
    account: Dict[str, Any]
    tenant: Dict[str, Any]
    tenant_unit: Dict[str, Any]
    permissions: List[str]
    plan: Dict[str, Any]
    

class CloudflareAPIClient:

    BASE_URL = "https://api.cloudflare.com/client/v4/"

    def __init__(self, auth_key, zone_id):
        logger.debug("Initializing CFClient")
        self.auth_key = auth_key
        self.zone_id = zone_id
        self._client: CloudFlare.CloudFlare = CloudFlare.CloudFlare(
                debug=settings.DEBUG,
                token=settings.AUTH_KEY
                )

    def _get_zones(self) -> List[CloudflareDomain]:
        """
        Zones in cloudflare are essentially the domains
        with all the related settings
        """
        logger.debug(f"Getting zones/domains from Cloudflare")
        try:
            zones = self._client.zones.get()
        except CloudFlare.exceptions.CloudFlareAPIError as e:
            logger.error(f"api call from '{self._get_zones.__name__}' failed")
            exit("/zones %d %s - api call failed" % (e, e))
        except Exception as e:
            logger.error(f"api call from '{self._get_zones.__name__}' failed")
            exit("_get_zones - %s - api call failed" % (e))

        return [CloudflareDomain(**zone) for zone in zones]

    def _get_dns_records_from_domain_id(self, domain_id: str) -> List[CloudflareDNSRecord]:
        dns_records: List[CloudflareDNSRecord] = [] 

        try:
            response = self._client.zones.dns_records.get(domain_id)
            dns_records.extend([CloudflareDNSRecord(**record) for record in response])
        except CloudFlare.exceptions.CloudFlareAPIError as e:
            logger.error(f"api call from '{self._get_dns_records_from_domain_id.__name__}' failed")
            exit("/zones %d %s - api call failed" % (e, e))
        except Exception as e:
            logger.error(f"api call from '{self._get_dns_records_from_domain_id.__name__}' failed")
            exit("_get_dns_records_from_domain_id - %s - api call failed" % (e))

        return dns_records

    def get_dns_records(self):
        logger.debug(f"Getting records from Cloudflare")
        domains = self._get_zones()

        dns_records: List[CloudflareDNSRecord] = []

        for domain in domains:
            logger.debug(f"getting DNS records from {domain.name}")
            response = self._get_dns_records_from_domain_id(domain.id)
            dns_records.extend(response)

        return dns_records

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

