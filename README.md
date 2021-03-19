# alert-aws-health
This is an automation notification tool for sending AWS Health Alerts to Slack and E-mail

## Setup
---
### Slack Configuration
_You will need to have access to add a new channel and app to your Slack workspace_
1. Create a new or use a existing channel for events (i.e aws_events)
2. In your browser go to: _workspace-name.slack.com/apps_ where _workspace-name_ is the name of your slack workspace.
3. In the search bar, search for incoming WebHooks and click on it.
4. Click on add to Slack.
5. From the dropdown click on the channel you created in step 1 and click add incoming WebHook integration.
6. From this page you can change the name of the WebHook (i.e AWS Bot), the icon/emoji to use etc
7. Copy the _WebHook URL_ we will need it for the deployment.

###  Deployment
1. Upload the `healthnotification_lambda.zip` to a bucket in S3
2. In your AWS console go to CloudFormation
3. Create a Stack with the `healthnofication.yml` template
4. Enter the _WebHook URL_ copied from the [slack configuration section](#slack-configuration), as the value for the _HookURL_ parameter.
5. Enter the _email address_ that will receive the notification for health events, as the value for the _Email_ parameter.
6. Enter the _S3 Bucket_ the from **Step 1**, as the value for the _S3Bucket_ parameter.
7. Finally enter the `healthnotification_lambda.zip` or the path to the file if nested in the S3 bucket, as the value for _S3Key_ parameter and Deploy.
8. Resources created include:
   - A Lambda function role: this gives the lambda the necessary permission to execute
   - A Lambda function: receives an event form the cloudwatch events and formats the message and sends it to the appropriate destinations.
   - CloudwatchEvent/EventBridge Rule: Monitors for AWS Health events and triggers the lambda function.
   - Lambda invoke permission: gives cloudwatch event/EventBridge permission to invoke the lambda function.
   - SNS Topic: An SNS topic receives the formatted message from lambda and sends it to subscribers
   - SNS Subscription: An email subscription that is notified when there is a health event 

NOTE: After Deployment you have to **CONFIRM SUBSCRIPTION** from the email address provided to start receiving email notifications