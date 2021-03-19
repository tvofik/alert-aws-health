import urllib3
import json
import logging
import boto3
import os


logger = logging.getLogger()
logger.setLevel(logging.INFO)

http = urllib3.PoolManager()

topic_arn = os.environ['TopicArn']


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
