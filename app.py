import aws_cdk as cdk

from infrastructure.hosted_zone_stack import HostedZoneStack
from infrastructure.cert_stack import CertStack
from infrastructure.website_stack import WebsiteStack


london = cdk.Environment(region='eu-west-2')
north_virginia = cdk.Environment(region='us-east-1')
DOMAIN = 'derner.co.uk'
DOMAIN_PREFIXES = [
    'www',
    'max'
]


app = cdk.App()

zone_stack = HostedZoneStack(
    app,
    'hosted-zone-stack',
    domain=DOMAIN,
    env=london,
)
cert_stack = CertStack(
    app,
    'cert-stack',
    domain=DOMAIN,
    domain_prefixes=DOMAIN_PREFIXES,
    hosted_zone=zone_stack.hosted_zone,
    # Certs have to be North Virginian, go figure
    env=north_virginia,
)
WebsiteStack(
    app,
    'website-stack',
    domain=DOMAIN,
    domain_prefixes=DOMAIN_PREFIXES,
    hosted_zone=zone_stack.hosted_zone,
    domain_cert=cert_stack.domain_cert,
    env=london,
)

app.synth()
