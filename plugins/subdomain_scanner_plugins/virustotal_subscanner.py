from helpers.http_request_helper import send_get_request
import json

# Environment Variables
import os 
from dotenv import load_dotenv
from pathlib import Path
enviroment_file_path= Path('./env/.env')
load_dotenv(dotenv_path=enviroment_file_path)

VIRUSTOTAL_API_URL= os.getenv("VIRUSTOTAL_API_URL")
# Environment Variables

def virustotal_subscanner(domain:str):
    subdomain_list= []
    virustotal_request_header= {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.35', 'X-Tool': 'vt-ui-main', 'X-VT-Anti-Abuse-Header': 'MTA3OTM2NjUwMjctWldOb2IzQnZkMlZ5LTE2MzExMTc3NDIuNjU12', 'Accept-Ianguage': 'en-US,en;q=0.9,es;q=0.8'
    }

    request_status_code, virustotal_search_response= send_get_request(VIRUSTOTAL_API_URL.format(domain), request_headers=virustotal_request_header)

    if request_status_code != 200:
        return subdomain_list
    
    virustotal_search_response= json.loads(virustotal_search_response.text)
    for found_subdomain in virustotal_search_response["data"]:
        subdomain_list.append(found_subdomain["id"])

    print('Virustotal Subdomain Scanner Done! Total Subdomains Found:', len(subdomain_list))
    return subdomain_list
