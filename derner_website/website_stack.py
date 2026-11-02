from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_certificatemanager as acm,
    aws_route53 as route53,
    CfnOutput,
    Environment,
)
from constructs import Construct

from .route53_records_construct import Route53Records


class WebsiteStack(Stack):

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            domain: str,
            domain_prefixes: list[str],
            hosted_zone: route53.HostedZone,
            domain_cert: acm.Certificate,
            env: Environment,
    ) -> None:
        """Final stack of the 3 stacks defining the website
        infrastructure. Allowing this stack the be separate to the TLS
        certificate and the hosted zone the certificate depends on.
        Letting you keep the routing separate from the website"""
        super().__init__(
            scope,
            construct_id,
            stack_name="DernerWebsite",
            env=env,
        )

        website_src = s3.Bucket(
            self,
            id='website-src',
            bucket_name=f'{domain}-src',
        )
        CfnOutput(
            self,
            'bucket',
            value=website_src.bucket_name
        )

        distribution = cloudfront.Distribution(
            self,
            id='website-dist',
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3BucketOrigin.with_origin_access_control(
                    website_src
                )
            ),
            default_root_object='index.html',
            domain_names=[
                domain,
                f'www.{domain}'
            ],
            certificate=domain_cert,
            error_responses=[
                # cloudfront gives 403 when user goes somewhere they
                # shouldn't
                cloudfront.ErrorResponse(
                    http_status=403,
                    response_page_path='/error.html'
                ),
            ],
        )
        CfnOutput(
            self,
            'dist-id',
            value=distribution.distribution_id
        )
        Route53Records(
            self,
            'derner-records',
            distribution=distribution,
            domain_prefixes=domain_prefixes,
            hosted_zone=hosted_zone
        )
