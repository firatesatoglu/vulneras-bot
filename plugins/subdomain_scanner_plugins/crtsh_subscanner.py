from helpers.http_request_helper import send_get_request
import json

# Environment Variables
import os 
from dotenv import load_dotenv
from pathlib import Path
enviroment_file_path= Path('./env/.env')
load_dotenv(dotenv_path=enviroment_file_path)

CRT_SH_URL= os.getenv("CRT_SH_URL")
# Environment Variables

def crt_sh_subscanner(domain:str):
    subdomain_list= []
    request_status_code, crtsh_search_response= send_get_request(CRT_SH_URL.format(domain), {})

    if request_status_code != 200:
        return subdomain_list
    
    crtsh_search_response= json.loads(crtsh_search_response.text)
    for found_subdomain in crtsh_search_response:
        found_subdomain_list= found_subdomain['name_value'].split('\n')
        for found_subdomain in found_subdomain_list:
            found_subdomain= found_subdomain.replace("www.", "").replace("*.", "")
            if found_subdomain not in subdomain_list:
                subdomain_list.append(found_subdomain)
   
    print('Crt.sh Subdomain Scanner Done! Total Subdomains Found:', len(subdomain_list))
    return subdomain_list
