import aws_cdk as cdk

from derner_website.derner_website_stack import DernerWebsiteStack


app = cdk.App()
DernerWebsiteStack(
    app,
    "DernerWebsiteStack",
    env=cdk.Environment(
        account='306403888274',
        region='eu-west-2'
    ),
)

app.synth()
