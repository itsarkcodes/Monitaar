import os
import requests
import schedule
import time
import pytz
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from datetime import datetime
from models import db, Website
from utils import parse_time_string, is_within_operational_hours
from dotenv import load_dotenv

load_dotenv()

slack_bot_token = os.environ.get('SLACK_BOT_TOKEN')
slack_channel_id = os.environ.get('SLACK_CHANNEL_ID')

client = WebClient(token=slack_bot_token)
ist = pytz.timezone('Asia/Kolkata')

def check_websites():
    print(f"Checking websites at {datetime.now(ist).strftime('%Y-%m-%d %H:%M:%S')}")
    websites = Website.query.all()
    down_websites = []
    for website in websites:
        # Parse times
        start_time = parse_time_string(website.start_time)
        end_time = parse_time_string(website.end_time)
        if is_within_operational_hours(start_time, end_time):
            status_code = check_website(website.url)
            if status_code != 200:
                down_websites.append({
                    'website': website.url,
                    'status_code': status_code,
                    'time': datetime.now(ist).strftime('%Y-%m-%d %H:%M:%S'),
                    'slack_user_ids': website.slack_user_ids.split(',') if website.slack_user_ids else [],
                    'tag_here': website.tag_here  # Pass the tag_here flag
                })
            else:
                print(f"{website.url} is up.")
        else:
            print(f"{website.url} is outside operational hours.")
    if down_websites:
        send_slack_message(down_websites)

def check_website(url):
    try:
        response = requests.get(url, timeout=10)
        return response.status_code
    except requests.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return None

def send_slack_message(down_websites):
    try:
        for website_info in down_websites:
            website = website_info['website']
            status_code = website_info['status_code']
            time_checked = website_info['time']
            slack_user_ids = website_info['slack_user_ids']
            tag_here = website_info.get('tag_here', False)
            
            # Build the user mentions
            if tag_here:
                user_mentions = '<!here>'  # Tag @here
            else:
                user_mentions = ' '.join([f'<@{user_id.strip()}>' for user_id in slack_user_ids if user_id.strip()])

            status_text = "No Response" if status_code is None else f"Status Code: {status_code}"

            blocks = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"{user_mentions}\n\n:rotating_light: *Website Down Alert* :rotating_light:"
                    }
                },
                {"type": "divider"},
                {
                    "type": "section",
                    "fields": [
                        {"type": "mrkdwn", "text": f"*Website:*\n<{website}|{website}>"},
                        {"type": "mrkdwn", "text": f"*Status:*\n{status_text}"},
                        {"type": "mrkdwn", "text": f"*Time:*\n{time_checked}"}
                    ]
                },
                {"type": "divider"},
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": "Please check the affected website."}
                }
            ]

            client.chat_postMessage(channel=slack_channel_id, blocks=blocks)
            print(f"Alert sent for {website}")
    except SlackApiError as e:
        print(f"Error sending message: {e.response['error']}")

def start_monitoring(app):
    with app.app_context():
        schedule.every(5).minutes.do(check_websites)
        while True:
            schedule.run_pending()
            time.sleep(1)
