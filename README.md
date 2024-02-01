# hfinder

![](assets/logo.png)

## Description

**Hosts Finder**

Help recon of hostnames from specific ASN(s) or CIDR(s), thanks to [https://bgp.he.net/](https://bgp.he.net/) and [https://www.robtex.com/](https://www.robtex.com/).

Can generate filtered /etc/hosts file based on the results.

## Installation

*You should have ~~Chromium~~ ([https://github.com/SergeyPirogov/webdriver_manager/issues/649](https://github.com/SergeyPirogov/webdriver_manager/issues/649)) or* ***Google Chrome*** *pre-installed on your system.*

```bash
pip install hfinder
```

*Or:*

```bash
git clone https://github.com/cosad3s/hfinder.git
sudo pip3 install .
```

## Usage

```bash
❯ hfinder -h
usage: hfinder [-h] [-c CIDR] [-a ASN] [--hosts] [--fqdn] [--filter FILTER]

Find hostnames from ASN or CIDR - Robtex x BGP.HE

options:
  -h, --help       show this help message and exit
  -c CIDR          CIDR(s) (Single or multiple separated by commas - Ex: 192.168.0.0/24 or 192.168.0.0/24,192.168.1.0/24)
  -a ASN           ASN(s) (Single or multiple separated by commas - Ex: AS1234 or AS1234,AS4561)
  --hosts          Generate /etc/hosts like file
  --fqdn           Only display found FQDN
  --filter FILTER  Filter FQDN against regex (Ex: ^.*example\.org$)
```

## Examples

Examples:

```bash
❯ hfinder -c 207.231.168.0/21
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
```

```bash
❯ hfinder -a AS26673
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
❯ hfinder -a AS26673 --hosts
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
❯ hfinder -a AS26673 --hosts --filter "^.*uber.com$"
207.231.168.151 backup.uber.com
207.231.168.160 team.uber.com
207.231.169.199 prj.usuppliers.uber.com
207.231.169.200 usuppliers.uber.com
```

```bash
❯ hfinder -c 207.231.168.0/21 --fqdn
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

```bash
❯ hfinder -a AS63948,AS63943,AS63086,AS399759,AS273797,AS26673,AS203351,AS19934,AS147183,AS136114,AS134981,AS134135 --hosts --filter "^(.*\.uber\.com|.*\.uberinternal\.com|.*\.ubereats\.com)$"
43.231.12.135 cn-pek1.uber.com
104.36.192.131 ussh.uberinternal.com bastion-sjc1.uber.com bastion02-sjc1.prod.uber.com
104.36.197.130 ussh.uberinternal.com bastion-geo.uber.com
104.36.195.187 ussh.uberinternal.com
104.36.195.188 ussh.uberinternal.com
104.36.196.133 ussh.uberinternal.com bastion-phx2.prod.uber.com bastion-geo.uber.com
104.36.192.244 ussh.uberinternal.com bastion-sjc1.uber.com bastion01-sjc1.prod.uber.com
104.36.195.186 ussh.uberinternal.com
104.36.197.131 ussh.uberinternal.com bastion-geo.uber.com
104.36.197.230 ussh.uberinternal.com bastion-geo.uber.com
104.36.197.129 ussh.uberinternal.com bastion-geo.uber.com
104.36.196.134 ussh.uberinternal.com bastion-phx2.prod.uber.com bastion-geo.uber.com
# ...
```
