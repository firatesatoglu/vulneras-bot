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

NESSUS_API_URL= os.getenv('NESSUS_API_URL')
NESSUS_ACCESS_KEY= os.getenv('NESSUS_ACCESS_KEY')
NESSUS_SECRET_KEY= os.getenv('NESSUS_SECRET_KEY')
# Environment Variables

nessus_request_header={'X-ApiKeys': f'accessKey={NESSUS_ACCESS_KEY}; secretKey={NESSUS_SECRET_KEY}', 'Content-Type': 'application/json'}
def api_get_requests(api_endpoint):
    response= requests.get(NESSUS_API_URL + api_endpoint, headers=nessus_request_header, verify=False)
    return response

def api_post_requests(api_endpoint, post_body):
    print(NESSUS_API_URL + api_endpoint)
    response= requests.post(NESSUS_API_URL + api_endpoint, headers=nessus_request_header, data=post_body, verify=False)
    return response

def start_scan(scan_name, targetlist):
    target_list= ', '.join(targetlist)
    api_endpoint= "/scans"
    post_body= {"uuid":"ad629e16-03b6-8c1d-cef6-ef8c9dd3c658d24bd260ef5f9e66",
                "plugins":{"SMTP problems":{"status":"enabled"},
                "Backdoors":{"status":"enabled"},
                "Rocky Linux Local Security Checks":{"status":"enabled"},
                "Ubuntu Local Security Checks":{"status":"enabled"},
                "Gentoo Local Security Checks":{"status":"enabled"},
                "Oracle Linux Local Security Checks":{"status":"enabled"},
                "RPC":{"status":"enabled"},
                "Gain a shell remotely":{"status":"enabled"}
                ,"Service detection":{"status":"enabled"},
                "DNS":{"status":"enabled"},
                "Mandriva Local Security Checks":{"status":"enabled"},
                "Junos Local Security Checks":{"status":"enabled"},
                "Misc.":{"status":"enabled"},
                "FTP":{"status":"enabled"},
                "Slackware Local Security Checks":{"status":"enabled"},
                "Default Unix Accounts":{"status":"enabled"},
                "AIX Local Security Checks":{"status":"enabled"},
                "SNMP":{"status":"enabled"},
                "OracleVM Local Security Checks":{"status":"enabled"},
                "CGI abuses":{"status":"enabled"},
                "Settings":{"status":"enabled"},
                "CISCO":{"status":"enabled"},
                "Tenable.ot":{"status":"enabled"},
                "Firewalls":{"status":"enabled"},
                "Databases":{"status":"enabled"},
                "Debian Local Security Checks":{"status":"enabled"},
                "Fedora Local Security Checks":{"status":"enabled"},
                "Netware":{"status":"enabled"},
                "Huawei Local Security Checks":{"status":"enabled"},
                "Windows : User management":{"status":"enabled"},
                "VMware ESX Local Security Checks":{"status":"enabled"},
                "Virtuozzo Local Security Checks":{"status":"enabled"},
                "CentOS Local Security Checks":{"status":"enabled"},
                "Peer-To-Peer File Sharing":{"status":"enabled"},
                "NewStart CGSL Local Security Checks":{"status":"enabled"},
                "General":{"status":"enabled"},
                "Policy Compliance":{"status":"enabled"},
                "Amazon Linux Local Security Checks":{"status":"enabled"},
                "Solaris Local Security Checks":{"status":"enabled"},
                "F5 Networks Local Security Checks":{"status":"enabled"},
                "Denial of Service":{"status":"enabled"},
                "Windows : Microsoft Bulletins":{"status":"enabled"},
                "SuSE Local Security Checks":{"status":"enabled"},
                "Palo Alto Local Security Checks":{"status":"enabled"},
                "Alma Linux Local Security Checks":{"status":"enabled"},
                "Red Hat Local Security Checks":{"status":"enabled"},
                "PhotonOS Local Security Checks":{"status":"enabled"},
                "HP-UX Local Security Checks":{"status":"enabled"},
                "CGI abuses : XSS":{"status":"enabled"},
                "FreeBSD Local Security Checks":{"status":"enabled"},
                "Windows":{"status":"enabled"},
                "Scientific Linux Local Security Checks":{"status":"enabled"},
                "MacOS X Local Security Checks":{"status":"enabled"},
                "Web Servers":{"status":"enabled"},
                "SCADA":{"status":"enabled"}},
                "credentials":{"add":{},"edit":{},"delete":[]},
                "settings":{"patch_audit_over_telnet":"no",
                "patch_audit_over_rsh":"no",
                "patch_audit_over_rexec":"no",
                "snmp_port":"161",
                "additional_snmp_port1":"161",
                "additional_snmp_port2":"161",
                "additional_snmp_port3":"161",
                "http_login_method":"POST",
                "http_reauth_delay":"",
                "http_login_max_redir":"0",
                "http_login_invert_auth_regex":"no",
                "http_login_auth_regex_on_headers":"no",
                "http_login_auth_regex_nocase":"no",
                "never_send_win_creds_in_the_clear":"yes",
                "dont_use_ntlmv1":"yes",
                "start_remote_registry":"no",
                "enable_admin_shares":"no",
                "start_server_service":"no",
                "ssh_known_hosts":"",
                "ssh_port":"22",
                "ssh_client_banner":"OpenSSH_5.0",
                "attempt_least_privilege":"no",
                "region_dfw_pref_name":"yes",
                "region_ord_pref_name":"yes",
                "region_iad_pref_name":"yes",
                "region_lon_pref_name":"yes",
                "region_syd_pref_name":"yes",
                "region_hkg_pref_name":"yes",
                "microsoft_azure_subscriptions_ids":"",
                "aws_ui_region_type":"Rest of the World",
                "aws_us_east_1":"",
                "aws_us_east_2":"",
                "aws_us_west_1":"",
                "aws_us_west_2":"",
                "aws_ca_central_1":"",
                "aws_eu_south_1":"",
                "aws_eu_west_1":"",
                "aws_eu_west_2":"",
                "aws_eu_west_3":"",
                "aws_eu_central_1":"",
                "aws_eu_north_1":"",
                "aws_af_south_1":"",
                "aws_ap_east_1":"",
                "aws_ap_northeast_1":"",
                "aws_ap_northeast_2":"",
                "aws_ap_northeast_3":"",
                "aws_ap_southeast_1":"",
                "aws_ap_southeast_2":"",
                "aws_ap_south_1":"",
                "aws_me_south_1":"",
                "aws_sa_east_1":"",
                "aws_use_https":"yes",
                "aws_verify_ssl":"yes",
                "max_compliance_output_length_kb":"",
                "log_whole_attack":"no",
                "enable_plugin_debugging":"no",
                "debug_level":"1",
                "enable_plugin_list":"no",
                "audit_trail":"use_scanner_default",
                "include_kb":"use_scanner_default",
                "custom_find_filepath_exclusions":"",
                "custom_find_filesystem_exclusions":"",
                "custom_find_filepath_inclusions":"",
                "reduce_connections_on_congestion":"no",
                "network_receive_timeout":"5",
                "max_checks_per_host":"5",
                "max_hosts_per_scan":"100",
                "max_simult_tcp_sessions_per_host":"",
                "max_simult_tcp_sessions_per_scan":"",
                "safe_checks":"yes",
                "stop_scan_on_disconnect":"no",
                "slice_network_addresses":"no",
                "auto_accept_disclaimer":"no",
                "scan.allow_multi_target":"no",
                "host_tagging":"yes",
                "trusted_cas":"",
                "allow_post_scan_editing":"yes",
                "reverse_lookup":"no",
                "log_live_hosts":"no",
                "display_unreachable_hosts":"no",
                "display_unicode_characters":"no",
                "report_verbosity":"Normal",
                "report_superseded_patches":"yes",
                "silent_dependencies":"yes",
                "oracle_database_use_detected_sids":"no",
                "scan_malware":"no",
                "samr_enumeration":"yes",
                "adsi_query":"yes",
                "wmi_query":"yes",
                "rid_brute_forcing":"no",
                "request_windows_domain_info":"no",
                "scan_webapps":"no",
                "start_cotp_tsap":"8",
                "stop_cotp_tsap":"8",
                "modbus_start_reg":"0",
                "modbus_end_reg":"16",
                "test_default_oracle_accounts":"no",
                "provided_creds_only":"yes",
                "smtp_domain":"example.com",
                "smtp_from":"nobody@example.com",
                "smtp_to":"postmaster@[AUTO_REPLACED_IP]",
                "av_grace_period":"0",
                "report_paranoia":"Normal",
                "thorough_tests":"no",
                "collect_identity_data_from_ad":"",
                "svc_detection_on_all_ports":"yes",
                "detect_ssl":"yes",
                "ssl_prob_ports":"All ports",
                "dtls_prob_ports":"None",
                "cert_expiry_warning_days":"60",
                "enumerate_all_ciphers":"yes",
                "check_crl":"no",
                "syn_scanner":"yes",
                "syn_firewall_detection":"Automatic (normal)",
                "udp_scanner":"no",
                "ssh_netstat_scanner":"yes",
                "wmi_netstat_scanner":"yes",
                "snmp_scanner":"yes",
                "only_portscan_if_enum_failed":"yes",
                "verify_open_ports":"no",
                "unscanned_closed":"no",
                "portscan_range":"default",
                "wol_mac_addresses":"",
                "wol_wait_time":"5",
                "scan_network_printers":"no",
                "scan_netware_hosts":"no",
                "scan_ot_devices":"no",
                "ping_the_remote_host":"yes",
                "arp_ping":"yes",
                "tcp_ping":"yes",
                "tcp_ping_dest_ports":"built-in",
                "icmp_ping":"yes",
                "icmp_unreach_means_host_down":"no",
                "icmp_ping_retries":"2",
                "udp_ping":"no",
                "test_local_nessus_host":"yes",
                "fast_network_discovery":"no",
                "emails":"",
                "filter_type":"and",
                "filters":[],"launch_now":"true","enabled":"false","name":f"{scan_name}",
                "description":"",
                "folder_id":3,"scanner_id":"1",
                "text_targets":f"{target_list}",
                "file_targets":""}}

    api_response= api_post_requests(api_endpoint, json.dumps(post_body))
    return api_response.text

def get_scan_folder():
    api_endpoint= "/scans?"
    api_response= api_get_requests(api_endpoint)
    scan_list= json.loads(api_response.text)
    
    scan_folder_informations= []
    for scan_information in scan_list['scans']:
        scan_folder_informations.append({
            "scan_name": scan_information['name'],
            "scan_id": scan_information['id']})

    return scan_folder_informations

def get_all_scan_info():
    api_endpoint= "/scans?"
    api_response= api_get_requests(api_endpoint)
    scan_list= json.loads(api_response.text)
    
    all_scan_information= []
    for scan_information in scan_list['scans']:
        all_scan_information.append({
            "scan_name": scan_information['name'],
            "scan_id": scan_information['id'],
            "scan_status": scan_information['status']})

    return all_scan_information

def create_report(scan_id):
    api_endpoint= f"/scans/{scan_id}/export"
    post_body= {"format": "nessus"}
    api_response= api_post_requests(api_endpoint, json.dumps(post_body))
    return api_response.text