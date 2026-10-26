from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
)
from constructs import Construct


class DernerWebsiteStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        website_src = s3.Bucket(
            self,
            id='website-src',
            bucket_name='derner-site',
        )

        cloudfront.Distribution(
            self,
            id="website-dist",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3BucketOrigin.with_origin_access_control(
                    website_src
                )
            ),
            default_root_object='index.html',
            domain_names=['derner.co.uk'],
            error_responses=[
                # cloudfront gives 403 when user goes somewhere they
                # shouldn't
                cloudfront.ErrorResponse(
                    http_status=403,
                    response_page_path='/error.html'
                ),
            ],
        )