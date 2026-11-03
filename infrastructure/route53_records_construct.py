from aws_cdk import (
    aws_cloudfront as cloudfront,
    aws_route53 as route53,
    aws_route53_targets as targets,
)
from constructs import Construct


class Route53Records(Construct):

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            distribution: cloudfront.Distribution,
            domain_prefixes: list[str],
            hosted_zone: route53.HostedZone,
    ) -> None:
        """A small Construct to keep the messy A and AAAA records out of
        sight"""
        super().__init__(
            scope,
            construct_id,
        )
        distribution_target = route53.RecordTarget.from_alias(
            targets.CloudFrontTarget(distribution)
        )
        if '' not in domain_prefixes:
            domain_prefixes.append('')
        for prefix in domain_prefixes:
            record_name_kwarg = {'record_name': prefix} if prefix else {}
            route53.ARecord(
                scope,
                f'A{prefix}',
                zone=hosted_zone,
                target=distribution_target,
                **record_name_kwarg
            )
            route53.AaaaRecord(
                scope,
                f'AAAA{prefix}',
                zone=hosted_zone,
                target=distribution_target,
                **record_name_kwarg
            )
