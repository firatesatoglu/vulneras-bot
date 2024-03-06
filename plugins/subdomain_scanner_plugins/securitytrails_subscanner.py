from helpers.http_request_helper import send_get_request
import json

# Environment Variables
import os 
from dotenv import load_dotenv
from pathlib import Path
enviroment_file_path= Path('./env/.env')
load_dotenv(dotenv_path=enviroment_file_path)

SECURITYTRAILS_API_URL= os.getenv("SECURITYTRAILS_API_URL")
SECURITYTRAILS_API_KEY= os.getenv("SECURITYTRAILS_API_KEY")
# Environment Variables

def securitytrails_subscanner(domain:str):
    subdomain_list= []
    securitytrails_request_header={"accept": "application/json", "APIKEY": SECURITYTRAILS_API_KEY}
    request_status_code, securitytrails_search_response= send_get_request(SECURITYTRAILS_API_URL.format(domain), request_headers=securitytrails_request_header)

    if request_status_code != 200:
        print(f'Try to get a valid API key from SecurityTrails')
        return subdomain_list
    
    securitytrails_search_response= json.loads(securitytrails_search_response.text)
    for found_subdomain in securitytrails_search_response["subdomains"]:
        subdomain_list.append(f"{found_subdomain}.{domain}")

    print('SecurityTrails Subdomain Scanner Done! Total Subdomains Found:', len(subdomain_list))
    return subdomain_list