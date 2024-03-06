from helpers.http_request_helper import send_get_request
import json

# Environment Variables
import os 
from dotenv import load_dotenv
from pathlib import Path
enviroment_file_path= Path('./env/.env')
load_dotenv(dotenv_path=enviroment_file_path)

SHODAN_API_URL= os.getenv("SHODAN_API_URL")
SHODAN_API_KEY= os.getenv("SHODAN_API_KEY")
# Environment Variables

def shodan_subscanner(domain:str):
    subdomain_list= []
    request_status_code, shodan_search_response= send_get_request(SHODAN_API_URL.format(domain, SHODAN_API_KEY), {})
    
    if request_status_code != 200:
        print(f'Try to get a valid API key from Shodan')
        return subdomain_list

    shodan_search_response= json.loads(shodan_search_response.text)
    for found_subdomain in shodan_search_response["subdomains"]:
        subdomain_list.append(f"{found_subdomain}.{domain}")

    print('Shodan.io Subdomain Scanner Done! Total Subdomains Found:', len(subdomain_list))
    return subdomain_list
