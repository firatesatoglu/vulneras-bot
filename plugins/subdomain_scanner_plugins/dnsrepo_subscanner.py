from helpers.http_request_helper import send_get_request
from bs4 import BeautifulSoup

# Environment Variables
import os 
from dotenv import load_dotenv
from pathlib import Path
enviroment_file_path= Path('./env/.env')
load_dotenv(dotenv_path=enviroment_file_path)

DNSREPO_API_URL= os.getenv("DNSREPO_API_URL")
# Environment Variables

def dnsrepo_subscanner(domain:str):
    subdomain_list= []
    request_status_code, dnsrepo_search_response= send_get_request(DNSREPO_API_URL.format(domain), {})

    if request_status_code != 200:
        return subdomain_list
    
    dnsrepo_html_response = BeautifulSoup(dnsrepo_search_response.text, 'html.parser')
    for found_subdomain in dnsrepo_html_response.find_all('a', href=True):
        if found_subdomain['href'].startswith('/?domain'):
            subdomain_list.append(found_subdomain.get_text().rstrip('.'))

    print('DnsRepo Subdomain Scanner Done! Total Subdomains Found:', len(subdomain_list))
    return subdomain_list