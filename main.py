#!./venv/bin/python3.12
import os
import time
import settings
import logging
from logger import logger
from storage import Storage, DNSRecord, save, read

from cf_client import CloudflareAPIClient, CloudflareDNSRecord

from typing import List

def main():

    logger.info("Starting pynamic_dns")
    cf_client = CloudflareAPIClient(settings.AUTH_KEY, settings.ZONE_ID)

    # get current ip from DNS
    dns_records: List[CloudflareDNSRecord] = cf_client.get_dns_records()
    logger.debug(f"got '{len(dns_records)}' DNS records from client")
    
    if len(dns_records) > 0:
        storage: Storage = read()

        if len(storage.dns_records) == 0:
           logging.debug("Saving initial storage data")
           for dns_record in dns_records:
               record = DNSRecord(
                       id=dns_record.id,
                       name=dns_record.name, 
                       domain=dns_record.zone_name, 
                       ip_address=dns_record.content, 
                       type=dns_record.type, 
                       proxied=dns_record.proxied
                )

               storage.dns_records.append(record)

           save(storage)


        TODO: since we need to access date frequiently we should use dicts for passing date, with record id and domain and as keys

        else:
            for dns_record in dns_records:
                for stored_record in storage.dns_records:
                    if stored_record.id == dns_record.id:
                        updated_record = DNSRecord(
                            id=dns_record.id,
                            name=dns_record.name, 
                            domain=dns_record.zone_name, 
                            ip_address=dns_record.content, 
                            update_ip_address=stored_record.update_ip_address,
                            type=dns_record.type, 
                            proxied=dns_record.proxied
                        )





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

def _get_current_server_ip() -> str:
    result = os.popen("curl -4 ifconfig.me").read()
    return result


def _setup():
    # setup project dir if not exists (/opt/pynamic_dns/)
    # create storage.json if not exists
    # create /opt/pynamic_dns/backups?
    pass


if __name__ == "__main__":
    main()
