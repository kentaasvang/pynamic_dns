
IPV4ENDPOINT = "https://api4.my-ip.io/v2/ip.json"
IPV6ENDPOINT = "https://api6.my-ip.io/v2/ip.json"


class MyIPResponse:
    success: bool
    ip: str
    ip_type: str


class MyIPv6Response:
    pass


class IPAddresses:
    IPv4: MyIPResponse
    IPv6: MyIPResponse


def get_ip_addresses() -> IPAddresses:
    ip_addresses = IPAddresses()
    ip_addresses.IPv4 = _get_ipv4_address()
    ip_addresses.IPv6 = _get_ipv6_address()
    return ip_addresses


def _get_ipv4_address() -> MyIPResponse:
    pass


def _get_ipv6_address() -> MyIPResponse:
    pass