#!./venv/bin/python3.12
import os
import time
import settings
from logger import logger
from storage import Storage, Domain, save

from cf_client import CFClient, CloudflareDNSRecord

from typing import List

def main():

    logger.info("Starting pynamic_dns")

    # get current public server ip
    current_server_ip = get_current_server_ip()
    logger.debug(f"current_server_ip: '{current_server_ip}'")

    cf_client = CFClient(settings.AUTH_KEY, settings.ZONE_ID)

    # get current ip from DNS
    # TODO: check db first
    dns_records: List[CloudflareDNSRecord] | CloudflareDNSRecord | None = cf_client.get_dns_records()
    
    if dns_records != None:
        domains = []
        if type(dns_records) == List[CloudflareDNSRecord]:
            for dns_record in dns_records:
                domains.append(Domain(dns_record.name, False, dns_record.content, dns_record.type, dns_record.proxied))

        elif type(dns_records) == CloudflareDNSRecord:
            domains.append(Domain(dns_records.name, False, dns_records.content, dns_records.type, dns_records.proxied))

        storage = Storage(domains = domains)
        save(storage)

"""
        for dns_record in dns_records:
            logger.info(f"Checking IP on '{dns_record.name}'")

            if dns_record.name not in settings.domains:
                logger.info(f"Skipping record: '{dns_record.name}'")
                continue

            if dns_record.content != current_server_ip:
                logger.info(f"Updating IP on '{dns_record.name}' to '{current_server_ip}'")
                result = cf_client.update_ip_address(dns_record, current_server_ip)

                if result:
                    logger.info(f"Successfully updated '{dns_record.name}'")
                else:
                    logger.warning(f"Something wen't wrong updating dns_record '{dns_record.name}'")

            logger.info(f"Finished checking '{dns_record.name}'")

    logger.info(f"Sleeping for {settings.SLEEP_IN_SECONDS}seconds")
    time.sleep(settings.SLEEP_IN_SECONDS)
  """  

def get_current_server_ip():
    result = os.popen("curl -4 ifconfig.me").read()
    return result


if __name__ == "__main__":
    main()
