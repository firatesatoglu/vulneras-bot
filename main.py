import telebot
import json
import time

import helpers.acunetix_helper as acunetix
import helpers.nessus_helper as nessus 
from plugins.subdomain_scanner import run_search
# Environment Variables
import os 
from dotenv import load_dotenv
from pathlib import Path
dotenv_path = Path('./env/.env')
load_dotenv(dotenv_path=dotenv_path)
TELEGRAM_BOT_TOKEN= os.getenv('TELEGRAM_BOT_TOKEN')
# Environment Variables

def check_exist_group(domain): 
    for target_group in acunetix.get_all_target_group():
        if target_group['Target Group'] == domain:
            return True
    return False

autonesacu_bot= telebot.TeleBot(TELEGRAM_BOT_TOKEN)
print("Bot started.. Bot info: ", autonesacu_bot.get_me())

@autonesacu_bot.message_handler(commands=['help'])
def send_help(message):
    autonesacu_bot.reply_to(message, "/help - This help message\n/target - Add target domain\n/createreport - Create report\n/downloadreport - Download report\n/listtargets - List all targets\n/listreports - List all reports")
        
@autonesacu_bot.message_handler(commands=['target'])
def target(message):
    message_remove_command= message.text.replace("/target", "")
    message_remove_space= message_remove_command.strip(" ")
    message_last= message_remove_space.split('\n') 
    
    for domain in message_last:
        if check_exist_group(domain): 
            autonesacu_bot.reply_to(message, f"This domain already exist in target group. I created new group with new name.")
            exist_domain_id= domain+"_"+str(time.time())
            acunetix_group_id=acunetix.create_target_group(exist_domain_id)
        else:
            autonesacu_bot.reply_to(message, f"Target group created for {domain}")
            acunetix_group_id=acunetix.create_target_group(domain)
        
        autonesacu_bot.reply_to(message, f"Subdomain scanning started for {domain}")
        subdomain_list= run_search(domain)
        subscanner_count= len(subdomain_list)
        if subscanner_count == 0:
            autonesacu_bot.reply_to(message, f"Not found any subdomain for {domain}")
            continue

        autonesacu_bot.reply_to(message, f"Found {subscanner_count} subdomains for {domain}")
        if subscanner_count > 490:
            for x in range(0, subscanner_count, 490):
                acunetix.add_multiple_target_to_target_group(subdomain_list[x:x+490], acunetix_group_id)
                acunetix.scan_target_group(acunetix_group_id)
                nessus.start_scan(domain, subdomain_list)
        else:
            acunetix.add_multiple_target_to_target_group(subdomain_list, acunetix_group_id)
            acunetix.scan_target_group(acunetix_group_id)
            nessus.start_scan(domain, subdomain_list)
        autonesacu_bot.reply_to(message, f"Acunetix and Nessus scan started for {domain}")
        time.sleep(20)

@autonesacu_bot.message_handler(commands=['listtargets'])
def list_target(message):
    target_info= json.dumps(acunetix.getallTargetGroup(), indent=4)
    if len(target_info) > 4095:
        for x in range(0, len(target_info), 4095):
            autonesacu_bot.reply_to(message, text=target_info[x:x+4095])
    else:
        autonesacu_bot.reply_to(message, text=target_info)

@autonesacu_bot.message_handler(commands=['createreport'])
def create_report(message):
    message_remove_command= message.text.replace("/createreport", "")
    message_remove_space= message_remove_command.strip(" ")
    message_last= message_remove_space.split('\n') 

    for domain in message_last:
        for targetGroup in acunetix.getallTargetGroup() and nessus.get_all_target():
            if targetGroup['Target Group'] == domain:
                nessus.create_report(targetGroup['Group ID'])
                acunetix.create_report(targetGroup['Group ID'])
                autonesacu_bot.reply_to(message, f"Report created for {domain}, after 2 minutes you can download report with /downloadreport command")

@autonesacu_bot.message_handler(commands=['downloadreport'])
def download_report(message):
    message_remove_command= message.text.replace("/downloadreport", "")
    message_remove_space= message_remove_command.strip(" ")
    message_last= message_remove_space.split('\n') 

    for domain in message_last:
        for report in acunetix.get_all_report_state():
            if report['Report Group'] == domain and report['Report Status'] == "completed":
                message_text= f"Report for {domain}\n HTML Report Download: {acunetix.ACUNETIXAPIURL+report['Report Download HTML']}\n PDF Report Download: {acunetix.ACUNETIXAPIURL+report['Report Download PDF']}"
                autonesacu_bot.reply_to(message, message_text)

@autonesacu_bot.message_handler(commands=['listreports'])
def list_report(message):
    report_info= json.dumps(acunetix.get_all_report_state(), indent=4)
    if len(report_info) > 4095:
        for x in range(0, len(report_info), 4095):
            autonesacu_bot.reply_to(message, text=report_info[x:x+4095])
    else:
        autonesacu_bot.reply_to(message, text=report_info)

autonesacu_bot.infinity_polling()