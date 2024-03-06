from helpers.http_request_helper import send_get_request
from bs4 import BeautifulSoup

# Environment Variables
import os 
from dotenv import load_dotenv
from pathlib import Path
enviroment_file_path= Path('./env/.env')
load_dotenv(dotenv_path=enviroment_file_path)

RAPIDDNS_URL= os.getenv("RAPIDDNS_URL")
# Environment Variables

def rapiddns_subscanner(domain:str):
    subdomain_list= []
    request_status_code, rapiddns_search_response= send_get_request(RAPIDDNS_URL.format(domain), {})

    if request_status_code != 200:
        return subdomain_list
    
    rapiddns_html_content= BeautifulSoup(rapiddns_search_response.content, 'html.parser')
    for table_content in rapiddns_html_content.find_all('tr'):
        if table_content.find('td'):
            subdomain_list.append(table_content.find('td').text)
    
    print('RapidDNS Subdomain Scanner Done! Total Subdomains Found:', len(subdomain_list))
    return subdomain_list