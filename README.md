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
1. In your AWS console go to CloudFormation
2. Create a Stack with the `slacknofication.yml` template
3. Enter the _WebHook URL_ copied from the [slack configuration section](#slack-configuration), as a the value for the _HookURL_ parameter and deploy.
4. Resources created include:
   - A Lambda function role: this gives the lambda the necessary permission to execute
   - A Lambda function: receives an event form the cloudwatch events and formats the message and sends it to the appropriate destinations.
   - CloudwatchEvent/EventBridge Rule: Monitors for AWS Health events and triggers the lambda function.
   - Lambda invoke permission: gives cloudwatch event/EventBridge permission to invoke the lambda function.
