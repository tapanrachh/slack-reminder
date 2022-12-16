from Reminder import Reminder
from slack_sdk.errors import SlackApiError
from slack_sdk import WebClient
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from slack_sdk.rtm_v2 import RTMClient
from flask import Flask

from praser import slack_parser
from storage import load_all
server = Flask(__name__)


client = WebClient(
    token="[SLACK-BOT-TOKEN]")
rtm = RTMClient(
    token="[SLACK-BOT-TOKEN]")
reminder = Reminder()


def send_reminder_message(channel_id, content, job_id, daily):
    try:
        client.chat_postMessage(
            channel=channel_id, text=f"Reminder : {content}", as_user="bot")
        if not daily:
            reminder.clear_one_timers(channel_id, job_id, scheduler)
    except SlackApiError as e:
        assert e.response["ok"] is False
        # str like 'invalid_auth', 'channel_not_found'
        assert e.response["error"]


scheduler = BackgroundScheduler(daemon=True)
scheduler.start()

if data := load_all():
    for key, items in data:
        for i in items:
            trigger = CronTrigger(
                year="*", month="*", day="*", hour=i["hh"], minute=i["mm"], second="0")
            job_id = i["job_id"]
            job_id = str(job_id)
            job_id = f"{key}-{job_id}"
            x = scheduler.add_job(
                send_reminder_message,
                trigger=trigger,
                args=[key, i["content"], job_id, i['daily']],
                name="daily reminder",
                id=job_id
            )


# Listen to incomming messages
@rtm.on("message")
def handle(client: RTMClient, event: dict):
    in_msg = event['text']
    channel_id = event['channel']
    out_msg = slack_parser(
        in_msg, channel_id, send_reminder_message, scheduler)

    client.web_client.chat_postMessage(
        channel=channel_id,
        text=out_msg,
        as_user="bot"
    )


rtm.start()
