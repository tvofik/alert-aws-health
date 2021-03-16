import urllib3
import json
import logging
import boto3
import os


logger = logging.getLogger()
logger.setLevel(logging.INFO)

http = urllib3.PoolManager()

topic_arn = os.environ['TopicArn']
url = os.environ['HookUrl']


def lambda_handler(event, context):
    sns_client = boto3.client('sns')

    category = event["detail"]["eventTypeCategory"]
    service = event['detail']['service']
    account = event['account']
    region = event["region"]
    start_time = event["detail"]["startTime"]
    end_time = '-' if event['detail'].get(
        'endTime') == None else event['detail'].get('endTime')
    eventcode = event["detail"]["eventTypeCode"]
    description = event['detail']['eventDescription'][0]['latestDescription']
    link = f"https://phd.aws.amazon.com/phd/home#/event-log?eventID={event['detail']['eventArn']}"
    resources = ", ".join(event['resources']) if event['resources'] else '-'

    # SEND TO SLACK
    msg = {
        "attachments": [
            {
                "fallback": f"AWS Health Notification [{category}]: <https://phd.aws.amazon.com/phd/home#/event-log?eventID={event['detail']['eventArn']}|Click here> for more details",
                "pretext": f"AWS Health Notification [{category}]: <https://phd.aws.amazon.com/phd/home#/event-log?eventID={event['detail']['eventArn']}|Click here> for more details",
                "color": "#ED2828" if category == "issue" else "#FCD33D" if category == "scheduledChange" else "#2292DC",
                "fields": [
                    {
                        "title": "Account",
                        "value": account,
                        "short": True
                    },
                    {
                        "title": "Region",
                        "value": region,
                        "short": True
                    },
                    {
                        "title": "Service",
                        "value": service,
                        "short": True
                    },
                    {
                        "title": "Category",
                        "value": category,
                        "short": True
                    },
                    {
                        "title": "Start Time",
                        "value": start_time,
                        "short": True
                    },
                    {
                        "title": "End Time",
                        "value": end_time,
                        "short": True
                    },
                    {
                        "title": "Event Code",
                        "value": eventcode,
                        "short": False
                    },
                    {
                        "title": "Message Description",
                        "value": f"{description}\n<{link}|Click Here> for more details",
                        "short": False
                    },
                    {
                        "title": "Affected Resources",
                        "value": resources,
                        "short": False
                    }
                ]
            }
        ]
    }

    logger.info(msg)
    encoded_msg = json.dumps(msg).encode('utf-8')

    try:
        resp = http.request('POST', url, body=encoded_msg)
        logger.info({'Message': 'Message posted to slack',
                     'status_code': resp.status, 'response': resp.data})
    except Exception as e:
        logger.error(f"Exception: {e}")

    # SEND TO SNS TOPIC
    try:
        message_subject = f'AWS Health Notification: {category} - {service}'
        message_body = f"Hello,\nAt {start_time}, there was a Health event with {service} service in AWS account {account}.\nRegion: {region}\nService: {service}\nCategory: {category}\nStart Time: {start_time}\nEnd Time: {end_time}\nEvent Code: {eventcode}\nMessage Description: {description}.\nAffected Resources: {resources}\nClick link for more details: {link}\n"
        logger.info({'subject': message_subject, 'body': message_body})
        sns_response = sns_client.publish(
            TopicArn=topic_arn, Message=message_body, Subject=message_subject)
        logger.info({'Message': 'Message sent to SNS topic...',
                     'response': sns_response})
    except Exception as e:
        logger.error(f"Exception: {e}")
