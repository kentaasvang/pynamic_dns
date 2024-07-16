
# NEXT STEPS
# ADD UNIT TESTS, MAKE SURE EVERYTHING WORKS
# THEN INTEGRATE INTO THE MAIN APP, ALSO WITH TESTS IF NATURAL
import requests

from pydantic import BaseModel

IPV4ENDPOINT = "https://api4.my-ip.io/v2/ip.json"
IPV6ENDPOINT = "https://api6.my-ip.io/v2/ip.json"


class MyIPResponse(BaseModel):
    success: bool
    ip: str
    type: str


class IPAddresses:
    IPv4: MyIPResponse
    IPv6: MyIPResponse


def get_ip_addresses() -> IPAddresses:
    ip_addresses = IPAddresses()
    ip_addresses.IPv4 = _get_ip_address()
    ip_addresses.IPv6 = _get_ip_address(ipv6=True)
    return ip_addresses


def _get_ip_address(ipv6: bool = False) -> MyIPResponse:
    endpoint = IPV6ENDPOINT if ipv6 else IPV4ENDPOINT
    result = requests.get(endpoint)    

    if result.status_code == requests.status_codes.codes.too_many_requests:
        return MyIPResponse(success=False, ip="", type="")

    if result.status_code == requests.status_codes.codes.ok:
        return MyIPResponse(**result.json())

    return MyIPResponse(success=False, ip="", type="")
