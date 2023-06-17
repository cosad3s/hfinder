#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
from bs4 import BeautifulSoup
import requests
import sys
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

requests.packages.urllib3.disable_warnings() 

def main():
    parser = argparse.ArgumentParser(description='Find hostnames from ASN or CIDR - Robtex x BGP.HE')
    parser.add_argument('-c', type=str, required=False, dest='cidr', help = "CIDR (Ex: 192.168.0.0/24)")
    parser.add_argument('-a', type=str, required=False, dest='asn', help = "ASN (Ex: AS1234)")
    args = parser.parse_args()
    hostnames = set()
    if (args.cidr):
        validate_cidr(args.cidr)
        hostnames.update(search_cidr(args.cidr))
    elif (args.asn):
        validate_asn(args.asn)
        ranges = search_asn(args.asn)
        for r in ranges:
            hostnames.update(search_cidr(r))
            time.sleep(1)
    else:
        fail()
    for h in hostnames:
        print(h)
    
def validate_cidr(cidr):
    cidr_regex = "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?:/\d{1,2}|)"
    m = re.search(cidr_regex,cidr)
    if not m:
        fail()

def validate_asn(asn):
    asn_regex = "^AS\d+$"
    m = re.search(asn_regex,asn)
    if not m:
        fail()

def search_asn(asn):
    bgphe_url = "https://bgp.he.net/"
    uri = asn

    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(str(bgphe_url)+uri)

    try:
        element_present = EC.presence_of_element_located((By.ID, 'table_prefixes4'))
        WebDriverWait(driver, 10).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")
    finally:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        table = soup.find_all(id='table_prefixes4')[0]
        links = table.find_all("a", href=True)
        
        filtered_links = [link["href"] for link in links if link["href"].startswith("/net/")]

        ranges = []
        for link in filtered_links:
            ranges.append(link.replace("/net/",""))
        
        return ranges

def search_cidr(cidr):
    robtex_url = "https://www.robtex.com/cidr/"
    uri = cidr.replace("/","-")

    session = requests.Session()
    response = session.get(str(robtex_url)+uri, verify=False)
    if (response.status_code != 200):
        fail()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    links = soup.find_all("a", href=True)
    filtered_links = [link["href"] for link in links if link["href"].startswith("https://www.robtex.com/dns-lookup/")]

    hostnames = []
    for link in filtered_links:    
        hostnames.append((link.replace("https://www.robtex.com/dns-lookup/","")))
    
    return hostnames

def fail():
    print("[-] Error with given parameters")
    sys.exit()

if __name__ == '__main__':
    main()