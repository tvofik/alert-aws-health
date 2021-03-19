# alert-aws-health
This is an automation notification tool for sending AWS Health Alerts to Slack and E-mail.
###  Deployment
1. In your AWS console go to CloudFormation
2. Create a Stack with the `healthnofication_sns.yml` template
3. Enter the _email address_ that will receive the notification for health events, as the value for the _Email_ parameter.
4. Resources created include:
   - A Lambda function role: this gives the lambda the necessary permission to execute
   - A Lambda function: receives an event form the cloudwatch events and formats the message and sends it to the appropriate destinations.
   - CloudwatchEvent/EventBridge Rule: Monitors for AWS Health events and triggers the lambda function.
   - Lambda invoke permission: gives cloudwatch event/EventBridge permission to invoke the lambda function.
   - SNS Topic: An SNS topic receives the formatted message from lambda and sends it to subscribers
   - SNS Subscription: An email subscription that is notified when there is a health event
  
**NOTE**: _After Deployment you have to **CONFIRM SUBSCRIPTION** from the email address provided to start receiving email notifications._