from helpers.http_request_helper import send_get_request
import json

# Environment Variables
import os 
from dotenv import load_dotenv
from pathlib import Path
enviroment_file_path= Path('./env/.env')
load_dotenv(dotenv_path=enviroment_file_path)

WHOXML_API_URL= os.getenv("WHOXML_API_URL")
WHOXML_API_KEY= os.getenv("WHOXML_API_KEY")
# Environment Variables

def whoxml_subscanner(domain:str):
    subdomain_list= []
    request_status_code, whoxml_search_response= send_get_request(WHOXML_API_URL.format(domain, WHOXML_API_KEY), {})

    if request_status_code != 200:
        print(f'Try to get a valid API key from WhoXML')
        return subdomain_list
    
    whoxml_search_response= json.loads(whoxml_search_response.text)
    for found_subdomain in whoxml_search_response["result"]["records"]:
        subdomain_list.append(found_subdomain['domain'])

    print('Whoxml Subdomain Scanner Done! Total Subdomains Found:', len(subdomain_list))
    return subdomain_list
