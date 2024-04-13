#!./venv/bin/python3.12

import os
import time
import requests
import settings
import logging

from cf_client import CFClient

def main():

    if not settings.CURRENT_IP:
        ipv4_file_path = os.path.join("data", "IPV4.txt")

        if os.path.exists(ipv4_file_path):
            with open(ipv4_file_path, "r") as ipv4_file:
                print(f"setting ip-address from {ipv4_file_path}")
                CURRENT_IP = ipv4_file.read()
                print(f"current IP is {CURRENT_IP}")
        else:
            CURRENT_IP = get_current_server_ip()
            with open(ipv4_file_path, "w") as ipv4_file:
                print(f"writing IP address to {ipv4_file_path}")
                ipv4_file.write(CURRENT_IP)
                print(f"current IP is {CURRENT_IP}")


def get_current_server_ip():
    result = os.popen("curl -4 ifconfig.me").read()
    return result

cf_client = CFClient(settings.AUTH_KEY, settings.ZONE_ID)

"""
while True:
    # Get the current IP address
    current_ip = get_current_server_ip()
    print(current_ip)

    dns_records = cf_client.get_dns_records()
    print(dns_records)
    for dns_record in dns_records["result"]:
        if dns_record["name"] in settings.domains:
            if dns_record["content"] != current_ip:
                print("Changing IP for", dns_record["name"])
                res = cf_client.change_ip(dns_record["name"], current_ip)
            else:
                print("IP for", dns_record["name"], "is already correct")
    # Sleep for 6 hours
    time.sleep(2000)
"""

if __name__ == "__main__":
    main()
