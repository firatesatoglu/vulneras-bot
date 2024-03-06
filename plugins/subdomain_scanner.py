from plugins.subdomain_scanner_plugins.bevigil_subscanner import bevigil_subscanner
from plugins.subdomain_scanner_plugins.crtsh_subscanner import crt_sh_subscanner
from plugins.subdomain_scanner_plugins.dnsrepo_subscanner import dnsrepo_subscanner
from plugins.subdomain_scanner_plugins.hackertarget_subscanner import hackertarget_subscanner
from plugins.subdomain_scanner_plugins.rapiddns_subscanner import rapiddns_subscanner
from plugins.subdomain_scanner_plugins.securitytrails_subscanner import securitytrails_subscanner
from plugins.subdomain_scanner_plugins.shodan_subscanner import shodan_subscanner
from plugins.subdomain_scanner_plugins.sslmate_subscanner import sslmate_subscanner
from plugins.subdomain_scanner_plugins.subdomainfinderio_subscanner import subdomainfinderio_subscanner
from plugins.subdomain_scanner_plugins.threadcrowd_subscanner import threadcrowd_subscanner
from plugins.subdomain_scanner_plugins.virustotal_subscanner import virustotal_subscanner
from plugins.subdomain_scanner_plugins.webarchive_subscanner import webarchive_subscanner
from plugins.subdomain_scanner_plugins.whoxml_subscanner import whoxml_subscanner

from datetime import datetime
import argparse
import pprint

# import socket
# def get_ip_address(subdomain):
#     try: return socket.gethostbyname(subdomain)
#     except: return None

def run_search(keyword):
    subdomain_list = []

    subdomain_list.extend(bevigil_subscanner(keyword))
    subdomain_list.extend(crt_sh_subscanner(keyword))
    subdomain_list.extend(dnsrepo_subscanner(keyword))
    subdomain_list.extend(hackertarget_subscanner(keyword))
    subdomain_list.extend(rapiddns_subscanner(keyword))
    subdomain_list.extend(securitytrails_subscanner(keyword))
    subdomain_list.extend(shodan_subscanner(keyword))
    subdomain_list.extend(sslmate_subscanner(keyword))
    subdomain_list.extend(subdomainfinderio_subscanner(keyword))
    subdomain_list.extend(threadcrowd_subscanner(keyword))
    subdomain_list.extend(virustotal_subscanner(keyword))
    subdomain_list.extend(webarchive_subscanner(keyword))
    subdomain_list.extend(whoxml_subscanner(keyword))

    subdomain_list= list(set(subdomain_list))
    subdomain_list.sort()

    return subdomain_list