from aws_cdk import (
    Stack,
    aws_route53 as route53,
    Environment,
)
from constructs import Construct


class HostedZoneStack(Stack):

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            domain: str,
            env: Environment,
    ) -> None:
        """A bootstrapping stack that establishes the hosted zone up front
        without getting into it with the TLS certificate"""
        super().__init__(
            scope,
            construct_id,
            stack_name="DernerHostedZone",
            env=env,
        )

        self.hosted_zone = route53.HostedZone(
            self,
            'derner-zone',
            zone_name=domain
        )
