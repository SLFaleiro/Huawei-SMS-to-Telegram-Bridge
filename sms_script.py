#!/usr/bin/python3
import requests
import xml.etree.ElementTree as ET
import logging

# Setup logging
logging.basicConfig(filename='sms_bridge.log', level=logging.INFO)

# Constants
SMS_SERVER_URL = 'http://192.168.8.1'
TELEGRAM_BOT_TOKEN = 'TELEGRAM BOT TOKEN Here'
TELEGRAM_CHAT_ID = 'TELEGRAM CHAT ID Here'

def get_session_token_info():
    response = requests.get(f'{SMS_SERVER_URL}/api/webserver/SesTokInfo')
    root = ET.fromstring(response.content)
    session_id = root.findtext('SesInfo')
    token = root.findtext('TokInfo')
    return session_id, token

def get_sms_list(session_id, token):
    headers = {
        'Cookie': session_id,
        '__RequestVerificationToken': token
    }
    data = '''<?xml version="1.0" encoding="UTF-8"?>
    <request>
        <PageIndex>1</PageIndex>
        <ReadCount>20</ReadCount>
        <BoxType>1</BoxType>
        <SortType>0</SortType>
        <Ascending>0</Ascending>
        <UnreadPreferred>0</UnreadPreferred>
    </request>'''
    response = requests.post(f'{SMS_SERVER_URL}/api/sms/sms-list', headers=headers, data=data)
    return response.content

def send_message_to_telegram(chat_id, text):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    response = requests.post(url, data=payload)
    return response.ok

def delete_sms(session_id, token, index):
    session_id, token = get_session_token_info()
    headers = {
        'Cookie': session_id,
        '__RequestVerificationToken': token
    }
    print(session_id +"\n"+ token +"\n"+ index)
    data = f'''<?xml version="1.0" encoding="UTF-8"?>
    <request>
        <Index>{index}</Index>
    </request>'''
    response = requests.post(f'{SMS_SERVER_URL}/api/sms/delete-sms', headers=headers, data=data)
    return response.ok

def process_messages():
    session_id, token = get_session_token_info()
    sms_list_xml = get_sms_list(session_id, token)

    root = ET.fromstring(sms_list_xml)
    for message in root.findall('.//Message'):
        phone = message.findtext('Phone')
        content = message.findtext('Content')
        index = message.findtext('Index')

        # Log the message
        logging.info(f'Received message from {phone}: {content}')

        # Send message to telegram
        if send_message_to_telegram(TELEGRAM_CHAT_ID, f'Message from {phone}: {content}'):
            logging.info(f'Successfully sent message to Telegram from {phone}')

            # Delete the message from SMS server
            if delete_sms(session_id, token, index):
                logging.info(f'Successfully deleted message with index {index}')
            else:
                logging.warning(f'Failed to delete message with index {index}')
        else:
            logging.warning(f'Failed to send message to Telegram from {phone}')

if __name__ == "__main__":
    process_messages()
