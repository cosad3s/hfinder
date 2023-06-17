# Hostnames finder

## Description

Help enumeration of hostnames from specific ASN or CIDR, thanks to [https://bgp.he.net/](https://bgp.he.net/) and [https://www.robtex.com/](https://www.robtex.com/).

## Usage

```bash
pip install -r requirements
```

```bash
python3 ./hf.py -h
usage: hf.py [-h] [-c CIDR] [-a ASN]

Find hostnames from ASN or CIDR - Robtex x BGP.HE

options:
  -h, --help  show this help message and exit
  -c CIDR     CIDR (Ex: 192.168.0.0/24)
  -a ASN      ASN (Ex: AS1234)
```

Examples:

```bash
python3 hf.py -a AS26673
vpn-west.uberinternal.com
itelogs.uberinternal.com
backup.uberinternal.com
backup.uber.com
munki.uberinternal.com
team.uber.com
team.uberinternal.com
jds.uberinternal.com
jds-staging.uberinternal.com
...
```

```bash
python3 hf.py -c 207.231.168.0/21
vpn-west.uberinternal.com
itelogs.uberinternal.com
backup.uberinternal.com
backup.uber.com
munki.uberinternal.com
team.uber.com
team.uberinternal.com
jds.uberinternal.com
jds-staging.uberinternal.com
chef.uberinternal.com
scout.uberinternal.com
tableau.uberinternal.com
vpn-east.uberinternal.com
prj.usuppliers.uber.com
usuppliers.uber.com
vpn-west.uberatc.com
...
