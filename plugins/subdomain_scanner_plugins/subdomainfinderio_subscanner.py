from helpers.http_request_helper import send_post_request
from bs4 import BeautifulSoup

# Environment Variables
import os 
from dotenv import load_dotenv
from pathlib import Path
enviroment_file_path= Path('./env/.env')
load_dotenv(dotenv_path=enviroment_file_path)

SUBDOMAINFINDER_IO_URL= os.getenv("SUBDOMAINFINDER_IO_URL")
# Environment Variables

def subdomainfinderio_subscanner(domain):
    subdomain_list= []
    request_headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    post_data= { 
        'domain': domain, 
        'scan': '',}

    request_status_code, subdomainfinderio_search_response= send_post_request(SUBDOMAINFINDER_IO_URL, post_data=post_data, request_headers=request_headers)
    
    if request_status_code != 200:
        return subdomain_list

    subfinderio_html_content= BeautifulSoup(subdomainfinderio_search_response.text, 'html.parser')
    subfinderio_html_table= subfinderio_html_content.find('table')
    if subfinderio_html_table:
        for all_table_row in subfinderio_html_table.find_all('tr')[1:]:
            columns= all_table_row.find_all('td')
            found_subdomain= columns[0].text.strip()
            subdomain_list.append(found_subdomain)

        print('Subdomainfinder.io Subdomain Scanner Done! Total Subdomains Found:', len(subdomain_list))
        return subdomain_list
    
    else:
        print('Subdomainfinder.io Subdomain Scanner Done! Total Subdomains Found:', len(subdomain_list))
        return subdomain_list