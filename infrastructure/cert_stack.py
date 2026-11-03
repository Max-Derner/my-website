from aws_cdk import (
    Stack,
    aws_certificatemanager as acm,
    aws_route53 as route53,
    Environment,
)
from constructs import Construct


class CertStack(Stack):
    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            domain: str,
            domain_prefixes: list[str],
            hosted_zone: route53.HostedZone,
            env: Environment,
    ):
        """A stack to publish a public certificate for the website.
        Stack only contains the certificate in case the cert hangs and
        biffs the deployment. This way it won't try to roll back your
        hosted zone as well"""
        super().__init__(
            scope,
            construct_id,
            stack_name="DernerCertificate",
            env=env,
        )

        self.domain_cert = acm.Certificate(
            self,
            'derner-cert',
            certificate_name="derner-cert",
            domain_name=domain,
            subject_alternative_names=[
                f'{prefix}.{domain}'
                for prefix in domain_prefixes
            ],
            validation=acm.CertificateValidation.from_dns(hosted_zone)
        )
