from helpers.http_request_helper import send_get_request
import json

# Environment Variables
import os 
from dotenv import load_dotenv
from pathlib import Path
enviroment_file_path= Path('./env/.env')
load_dotenv(dotenv_path=enviroment_file_path)

BEVIGIL_API_URL= os.getenv("BEVIGIL_API_URL")
BEVIGIL_API_KEY= os.getenv("BEVIGIL_API_KEY")
# Environment Variables

def bevigil_subscanner(domain:str):
    subdomain_list= []
    bevigil_request_header= {'X-Access-Token': BEVIGIL_API_KEY}
    request_status_code, bevigil_search_response= send_get_request(BEVIGIL_API_URL.format(domain, BEVIGIL_API_KEY), bevigil_request_header)

    if request_status_code != 200:
        print(f'Try to get a valid API key from Bevigil')
        return subdomain_list

    bevigil_search_response= json.loads(bevigil_search_response.text)
    for found_subdomain in bevigil_search_response["subdomains"]:
        subdomain_list.append(found_subdomain)
    
    print('Bevigil Subdomain Scanner Done! Total Subdomains Found:', len(subdomain_list))
    return subdomain_list
