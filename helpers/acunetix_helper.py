import json
import time
import argparse
import requests

from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# Environment Variables
import os 
from dotenv import load_dotenv
from pathlib import Path
dotenv_path = Path('./env/.env')
load_dotenv(dotenv_path=dotenv_path)

ACUNETIX_API_KEY= os.getenv("ACUNETIX_API_KEY")
ACUNETIX_API_URL= os.getenv("ACUNETIX_API_URL")
ACUNETIX_SCAN_PROFILE_ID= os.getenv("ACUNETIX_SCAN_PROFILE_ID")
ACUNETIX_DESCRIPTION= os.getenv("ACUNETIX_DESCRIPTION")
# Environment Variables

request_header= {'X-Auth': ACUNETIX_API_KEY, 'Content-Type': 'application/json'}
def api_get_requests(api_endpoint):
    response= requests.get(ACUNETIX_API_URL + api_endpoint , headers=request_header, verify=False)
    return response

def api_post_requests(api_endpoint, post_body):
    response= requests.post(ACUNETIX_API_URL + api_endpoint, headers=request_header, data=post_body, verify=False)
    return response

def create_target_group(group_name):
    api_endpoint= "/api/v1/target_groups"
    post_body= {
        "name": group_name,
        "description": ACUNETIX_DESCRIPTION
    }

    api_response= api_post_requests(api_endpoint, json.dumps(post_body))
    if api_response.status_code == 201:
        return json.loads(api_response.text)['group_id']
    else: 
        return f"Cannot create target group... Error: {api_response.text}"

def add_multiple_target_to_target_group(target_assets, target_group_id):
    api_endpoint= "/api/v1/targets/add"

    target_list= []
    for subdomain_address in '\n'.join(target_assets).split("\n"):
        target_list.append({
            "address":subdomain_address,
            "description":"Guthmaer Bot"})

    post_body= {
        "targets":target_list,
        "groups":[target_group_id]}

    api_response= api_post_requests(api_endpoint, json.dumps(post_body))
    if api_response.status_code == 201:
        return json.loads(api_response.text)['target_id']
    else:
        return f"Cannot add target to group... Error: {api_response.text}"

def scan_target_group(target_group_id):
    api_endpoint= f"/api/v1/target_groups/{target_group_id}/scan"
    post_body= {"profile_id":"11111111-1111-1111-1111-111111111111",
               "incremental":"false",
               "schedule": { 
                    "disable":"false",
                    "start_date":None,
                    "time_sensitive":"false"
                    }}

    api_response= api_post_requests(api_endpoint, json.dumps(post_body))
    if api_response.status_code == 201:
        return json.loads(api_response.text)['scan_id']

    else:
        return f"Cannot start scan... Error: {api_response.text}"

def get_all_target_info():
    api_endpoint= "/api/v1/targets"
    api_response= api_get_requests(api_endpoint)
    json_response= json.loads(api_response.text)

    target_informations= []
    for all_targets in json_response['targets']:
        target_name= all_targets['address']
        target_id= all_targets['target_id']
        target_scan_id= all_targets['last_scan_session_id']
        target_severity_score= all_targets['severity_counts']
        target_scan_status= all_targets['last_scan_session_status']
        target_scan_date= all_targets['last_scan_date']

        target_informations.append({
            "Target FQDN": target_name,
            "Scan Severity": target_severity_score,
            "Scan Status": target_scan_status,
            "Scan Date": target_scan_date,
            "Target ID": target_id,
            "Scan ID": target_scan_id})   

    return target_informations

def get_all_scans():
    api_endpoint= "/api/v1/scans"
    api_response= api_get_requests(api_endpoint)
    json_response= json.loads(api_response.text)

    scans_informations= []
    for all_scans in json_response['scans']:
        scan_id= all_scans['scan_id']
        scan_target_id= all_scans['target_id']
        scan_status= all_scans['current_session']['status']
        scan_target_url= all_scans['target']['address']    
        scan_severity_count= all_scans['current_session']['severity_counts']

        scans_informations.append({
            "Scan ID": scan_id,
            "Target ID": scan_target_id,
            "Scan Status": scan_status,
            "Target URL": scan_target_url,
            "Scan Severity": scan_severity_count})
    
    return scans_informations

def get_all_vulnerabilities():
    api_endpoint= "/api/v1/vulnerabilities"
    api_response= api_get_requests(api_endpoint)
    json_response= json.loads(api_response.text)

    vulnerabilities_informations= []
    for vulnerabilities in json_response['vulnerabilities']:
        vulnerability_id= vulnerabilities['vuln_id']
        
        vuln_detail= api_get_requests(f"/api/v1/vulnerabilities/{vulnerability_id}").json()
        vulnerability_target_url= vuln_detail['affects_url']
        vulnerability_name= vuln_detail['vt_name']
        vulnerability_detail= vuln_detail['details']
        vulnerability_request= vuln_detail['request']
    
        vulnerabilities_informations.append({
            "Vulnerability Name": vulnerability_name,
            "Vulnerability Target URL": vulnerability_target_url,
            "Vulnerability Detail": vulnerability_detail,
            "Vulnerability Request": vulnerability_request})
    
    return vulnerabilities_informations

def add_one_target(target_url):
    api_endpoint= "/api/v1/targets"
    post_body= {
        "address": target_url,
        "description": ACUNETIX_DESCRIPTION,
        "type": "default",
        "criticality": "20",
        "profile_id": ACUNETIX_SCAN_PROFILE_ID
    }

    api_response= api_post_requests(api_endpoint, json.dumps(post_body))
    if api_response.status_code == 201:
        return json.loads(api_response.text)['target_id']
    
    else:
        return f"Cannot add target... Error: {api_response.text}"

def add_target_to_group(group_id, target_id):
    api_endpoint= f"/api/v1/target_groups/{group_id}/targets"
    post_body= { "add":[target_id] }

    api_response= api_post_requests(api_endpoint, json.dumps(post_body))
    if api_response.status_code == 201:
        return target_id, group_id

    else:
        return f"Cannot add target to group... Error: {api_response.text}", None

def start_scan(target_id):
    api_endpoint= f"/api/v1/scans"
    post_body= {
    "profile_id": ACUNETIX_SCAN_PROFILE_ID,
    "incremental": "false",
    "schedule":
        {"disable": "false",
        "start_date": None,
        "time_sensitive": "false"},
    "user_authorized_to_scan": "yes",
    "target_id": target_id }

    api_response= api_post_requests(api_endpoint, json.dumps(post_body))
    if api_response.status_code == 201:
        return json.loads(api_response.text)['scan_id']

    else:
        return f"Cannot start scan... Error: {api_response.text}"

def get_all_target_group():
    api_endpoint= "/api/v1/target_groups"
    api_response= api_get_requests(api_endpoint)
    json_response= json.loads(api_response.text)

    get_all_target_info= []
    for group_detail in json_response['groups']:
        group_id= group_detail['group_id']
        group_name= group_detail['name']
        in_group_target= group_detail['target_count']
        group_vulnerability_count= group_detail['vuln_count']
        
        get_all_target_info.append({
            "Target Group": group_name,
            "Domain in Group": in_group_target,
            "Group ID": group_id,
            "Vulnerability Count": group_vulnerability_count})

    return get_all_target_info

def create_report(group_id):
    api_endpoint= "/api/v1/reports"
    post_body= { "template_id": "11111111-1111-1111-1111-111111111111",
    "source": {
        "list_type": "groups",
        "id_list": [group_id]}}
    
    api_response= api_post_requests(api_endpoint, json.dumps(post_body))
    if api_response.status_code == 201:
        return json.loads(api_response.text)['report_id']
    else:
        return f"Cannot create report... Error: {api_response.text}"

def get_all_report_state():
    api_endpoint= "/api/v1/reports"
    api_response= api_get_requests(api_endpoint)
    json_parsed_response= json.loads(api_response.text)

    report_info= []
    for report in json_parsed_response['reports']:
        report_download_html= report['download'][0]
        report_download_pdf= report['download'][1]
        report_group= report['source']['description']
        report_status= report['status']
        report_info.append({"Report Group":f"{report_group}","Report Status":f"{report_status}","Report Download HTML":f"{report_download_html}","Report Download PDF":f"{report_download_pdf}"})
        
    return report_info
