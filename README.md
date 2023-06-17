# Hostnames finder

## Description

Help enumeration of hostnames from specific ASN or CIDR, thanks to [https://bgp.he.net/](https://bgp.he.net/) and [https://www.robtex.com/](https://www.robtex.com/).
Can generate /etc/hosts file based on the results.

## Usage

```bash
pip install -r requirements
```

```bash
❯ python3 hf.py -h
usage: hf.py [-h] [-c CIDR] [-a ASN] [--hosts] [--fqdn]

Find hostnames from ASN or CIDR - Robtex x BGP.HE

options:
  -h, --help  show this help message and exit
  -c CIDR     CIDR (Ex: 192.168.0.0/24)
  -a ASN      ASN (Ex: AS1234)
  --hosts     Generate /etc/hosts like file
  --fqdn      Only display found FQDN
```

Examples:

```bash
❯ python3 hf.py -c 207.231.168.0/21
vpn-west.uberinternal.com:207.231.168.144
itelogs.uberinternal.com:207.231.168.148
backup.uberinternal.com:207.231.168.151
backup.uber.com:207.231.168.151
munki.uberinternal.com:207.231.168.155
team.uber.com:207.231.168.160
team.uberinternal.com:207.231.168.160
jds.uberinternal.com:207.231.168.162
jds-staging.uberinternal.com:207.231.168.163
chef.uberinternal.com:207.231.168.172
scout.uberinternal.com:207.231.168.174
tableau.uberinternal.com:207.231.168.202
vpn-east.uberinternal.com:207.231.169.144
prj.usuppliers.uber.com:207.231.169.199
usuppliers.uber.com:207.231.169.200
vpn-west.uberatc.com:207.231.171.36
...

```bash
❯ python3 hf.py -a AS26673
vpn-west.uberinternal.com:207.231.168.144
itelogs.uberinternal.com:207.231.168.148
backup.uberinternal.com:207.231.168.151
backup.uber.com:207.231.168.151
munki.uberinternal.com:207.231.168.155
team.uber.com:207.231.168.160
team.uberinternal.com:207.231.168.160
jds.uberinternal.com:207.231.168.162
jds-staging.uberinternal.com:207.231.168.163
chef.uberinternal.com:207.231.168.172
scout.uberinternal.com:207.231.168.174
tableau.uberinternal.com:207.231.168.202
vpn-east.uberinternal.com:207.231.169.144
prj.usuppliers.uber.com:207.231.169.199
usuppliers.uber.com:207.231.169.200
vpn-west.uberatc.com:207.231.171.36
```

```bash
❯ python3 hf.py -a AS26673 --hosts
207.231.168.144 vpn-west.uberinternal.com
207.231.168.148 itelogs.uberinternal.com
207.231.168.151 backup.uberinternal.com backup.uber.com
207.231.168.155 munki.uberinternal.com
207.231.168.160 team.uberinternal.com team.uber.com
207.231.168.162 jds.uberinternal.com
207.231.168.163 jds-staging.uberinternal.com
207.231.168.172 chef.uberinternal.com
207.231.168.174 scout.uberinternal.com
207.231.168.202 tableau.uberinternal.com
207.231.169.144 vpn-east.uberinternal.com
207.231.169.199 prj.usuppliers.uber.com
207.231.169.200 usuppliers.uber.com
207.231.171.36 vpn-west.uberatc.com
```

```bash
❯ python3 hf.py -c 207.231.168.0/21 --fqdn
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
```
