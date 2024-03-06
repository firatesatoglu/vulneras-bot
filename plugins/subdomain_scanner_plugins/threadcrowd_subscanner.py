from helpers.http_request_helper import send_get_request
from bs4 import BeautifulSoup

# Environment Variables
import os 
from dotenv import load_dotenv
from pathlib import Path
enviroment_file_path= Path('./env/.env')
load_dotenv(dotenv_path=enviroment_file_path)

THREADCROWD_API_URL= os.getenv("THREADCROWD_API_URL")
# Environment Variables

def threadcrowd_subscanner(domain:str):
    subdomain_list= []
    request_status_code, threadcrowd_search_response= send_get_request(THREADCROWD_API_URL.format(domain), {})

    if request_status_code != 200:
        return subdomain_list

    threadcrowd_html_response = BeautifulSoup(threadcrowd_search_response.text, 'html.parser')
    for found_subdomain in threadcrowd_html_response.find_all('a', href=True):
        if found_subdomain['href'].startswith('/?domain'):
            subdomain_list.append(found_subdomain.get_text().rstrip('.'))
    
    print('Threadcrowd Subdomain Scanner Done! Total Subdomains Found:', len(subdomain_list))
    return subdomain_list