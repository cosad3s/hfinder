#!/usr/bin/python3
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
    parser.add_argument('-c', type=str, required=False, dest='cidr', help = "CIDR(s) (Single or multiple separated by commas - Ex: 192.168.0.0/24 or 192.168.0.0/24,192.168.1.0/24)")
    parser.add_argument('-a', type=str, required=False, dest='asn', help = "ASN(s) (Single or multiple separated by commas - Ex: AS1234 or AS1234,AS4561)")
    parser.add_argument('--hosts', action="store_true", default=False, dest='hosts', help = "Generate /etc/hosts like file")
    parser.add_argument('--fqdn', action="store_true", default=False, dest='fqdn', help = "Only display found FQDN")
    parser.add_argument('--filter', type=str, required=False, dest='filter', help = "Filter FQDN against regex (Ex: ^.*example\.org$)")
    args = parser.parse_args()

    # Validate the filter before launching any search activities
    filter=""
    if args.filter:
        try:
            filter = re.compile(args.filter)
        except re.error:
            fail("Invalid filter: not a regex filter")
    
    # By default : for each value of the list, the key is FQDN and values are IPs
    final_findings = {}
    if (args.cidr):
        cidrs = args.cidr.split(",")
        for cidr in cidrs:
            validate_cidr(cidr)
            final_findings.update(search_cidr(cidr))
    elif (args.asn):
        asns = args.asn.split(",")
        for asn in asns:
            validate_asn(asn)
            ranges = search_asn(asn)
            for r in ranges:
                fresh_findings = search_cidr(r)
                for fresh_finding_fqdn in fresh_findings.keys():
                    actual_findings_ips = final_findings.get(fresh_finding_fqdn)
                    if actual_findings_ips is None:
                        actual_findings_ips = fresh_findings.get(fresh_finding_fqdn)
                    else:
                        actual_findings_ips.update(fresh_findings.get(fresh_finding_fqdn))
                    final_findings.update({fresh_finding_fqdn:actual_findings_ips})

                time.sleep(1)
    else:
        fail("Invalid given parameters. Should select -c or -a.")
    
    # Filter before display
    if filter:
        filtered_final_findings = {key: value for key, value in final_findings.items() if re.match(args.filter, key)}
        final_findings = filtered_final_findings

    # Reverse dictionnary to display as hosts file
    if args.hosts:
        result = {}
        index = 0;

        for ips in final_findings.values():
            for i in ips:
                fqdn_list = list(final_findings)[index]
                current_fqdn_list = result.get(i)
                if current_fqdn_list is None:
                    current_fqdn_list = set([fqdn_list])
                else:
                    current_fqdn_list.update([fqdn_list])
                result.update({i:current_fqdn_list})
            index = index + 1
        # Display as /etc/hosts file
        for item in result.keys():
            print(item + " " + " ".join(result.get(item)))
    else:
        if args.fqdn:
            for h in final_findings.keys():
                print(h)
        else:
            for h in final_findings.keys():
                print(h + ":" + " ".join(final_findings.get(h)))
    
def validate_cidr(cidr):
    cidr_regex = "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?:/\d{1,2}|)"
    m = re.search(cidr_regex,cidr)
    if not m:
        fail("Invalid CIDR: "+cidr)

def validate_asn(asn):
    asn_regex = "^AS\d+$"
    m = re.search(asn_regex,asn)
    if not m:
        fail("Invalid ASN: "+asn)

def search_asn(asn):
    bgphe_url = "https://bgp.he.net/"
    uri = asn

    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(str(bgphe_url)+uri)

    ranges = []
    try:
        element_present = EC.presence_of_element_located((By.ID, 'table_prefixes4'))
        WebDriverWait(driver, 10).until(element_present)
    except TimeoutException:
        return ranges
    finally:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        tables = soup.find_all(id='table_prefixes4');
        ranges = []
        if (len(tables) > 0):
            table = tables[0]
            links = table.find_all("a", href=True)
            
            filtered_links = [link["href"] for link in links if link["href"].startswith("/net/")]
    
            for link in filtered_links:
                ranges.append(link.replace("/net/",""))
        
        return ranges

def search_cidr(cidr):
    robtex_url = "https://www.robtex.com/cidr/"
    uri = cidr.replace("/","-")

    session = requests.Session()
    response = session.get(str(robtex_url)+uri, verify=False)
    if (response.status_code != 200):
        fail("Robtex invalid HTTP response: "+str(response.status_code))
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    links = soup.find_all("a", href=True)
    filtered_ip_links = [link["href"] for link in links if link["href"].startswith("https://www.robtex.com/ip-lookup/")]
    filtered_named_links = [link["href"] for link in links if link["href"].startswith("https://www.robtex.com/dns-lookup/")]

    hostnames = {}
    index = 0;
    for link in filtered_named_links:
        h = link.replace("https://www.robtex.com/dns-lookup/","")
        ip = filtered_ip_links[index].replace("https://www.robtex.com/ip-lookup/","")
        
        actual_findings = hostnames.get(h)
        if actual_findings is not None:
            actual_findings.update([ip])
        else:
            actual_findings = set([ip])
        hostnames.update({h:actual_findings})
        
        index = index + 1;
    
    return hostnames

def fail(msg):
    print("[-] Error: "+msg)
    sys.exit()

if __name__ == '__main__':
    main()