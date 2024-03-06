from helpers.http_request_helper import send_get_request
import json
import re

# Environment Variables
import os 
from dotenv import load_dotenv
from pathlib import Path
enviroment_file_path= Path('./env/.env')
load_dotenv(dotenv_path=enviroment_file_path)

WEBARCHIVE_API_URL= os.getenv("WEBARCHIVE_API_URL")
# Environment Variables

def webarchive_subscanner(domain: str):
    subdomain_list= set()
    request_status_code, webarchive_search_response= send_get_request(WEBARCHIVE_API_URL.format(domain), {})

    if request_status_code != 200:
        return subdomain_list
    
    webarchive_search_response= json.loads(webarchive_search_response.text)
    for webarchibe_data in webarchive_search_response:
        found_subdomain = re.match("(?:http[s]*\:\/\/)*(.*?)\.(?=[^\/]*\..{2,5})", webarchibe_data[2])
        if found_subdomain:
            remove_protocol= found_subdomain.group(0).replace("http://", "").replace("https://", "")
            clr_subdomain= f"{remove_protocol.split('/')[0]}{domain}".replace('@', '')
            subdomain_list.add(clr_subdomain)

    print('Webarchive Subdomain Scanner Done! Total Subdomains Found:', len(subdomain_list))
    return list(subdomain_list)
