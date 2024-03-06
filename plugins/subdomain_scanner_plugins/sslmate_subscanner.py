from helpers.http_request_helper import send_get_request
import json

# Environment Variables
import os 
from dotenv import load_dotenv
from pathlib import Path
enviroment_file_path= Path('./env/.env')
load_dotenv(dotenv_path=enviroment_file_path)

SSLMATE_API_URL= os.getenv("SSLMATE_API_URL")
SSLMATE_API_KEY= os.getenv("SSLMATE_API_KEY")
# Environment Variables

def sslmate_subscanner(domain:str):
    subdomain_list= []
    sslmate_request_header= {'API-Key': SSLMATE_API_KEY}
    request_status_code, sslmate_search_response= send_get_request(SSLMATE_API_URL.format(domain, SSLMATE_API_KEY), sslmate_request_header)

    if request_status_code != 200:
        print(f'Try to get a valid API key from SSLMate')
        return subdomain_list

    sslmate_search_response= json.loads(sslmate_search_response.text)
    for found_subdomain in sslmate_search_response:
        if domain in found_subdomain:
            subdomain_list.append(found_subdomain)

    print('SSLMate Subdomain Scanner Done! Total Subdomains Found:', len(subdomain_list))
    return subdomain_list