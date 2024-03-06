from helpers.http_request_helper import send_get_request
import requests

# Environment Variables
import os 
from dotenv import load_dotenv
from pathlib import Path
enviroment_file_path= Path('./env/.env')
load_dotenv(dotenv_path=enviroment_file_path)

HACKERTARGET_API_URL= os.getenv("HACKERTARGET_API_URL")
# Environment Variables

def hackertarget_subscanner(domain:str):
    subdomain_list= []
    request_status_code, hackertarget_search_response= send_get_request(HACKERTARGET_API_URL.format(domain), {})

    if request_status_code != 200:
        return subdomain_list
    elif "API count exceeded" in hackertarget_search_response.text:
        return subdomain_list

    hackertarget_search_response= hackertarget_search_response.text.split('\n')
    for found_subdomain in hackertarget_search_response:
        subdomain_list.append(found_subdomain.split(',')[0])

    print('HackerTarget Subdomain Scanner Done! Total Subdomains Found:', len(subdomain_list))
    return subdomain_list