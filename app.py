import aws_cdk as cdk

from derner_website.derner_website_stack import DernerWebsiteStack


app = cdk.App()
DernerWebsiteStack(
    app,
    "DernerWebsiteStack",
    env=cdk.Environment(
        account='123456789012',
        region='us-east-1'
    ),
)

app.synth()
