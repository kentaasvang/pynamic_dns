from whatsmyip.whatsmyip import get_ip_addresses


def test_get_ip_addresses():
    ip_addresses = get_ip_addresses()
    assert ip_addresses.IPv4 != None, "IPv4 is None"
    assert ip_addresses.IPv6 != None, "IPv6 is None"
    assert ip_addresses.IPv4.type.lower() == "ipv4", "IPv4 type is not IPv4"
    assert ip_addresses.IPv6.type.lower() == "ipv6", "IPv6 type is not IPv6"

