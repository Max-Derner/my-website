deploy-site:
    aws s3 sync ./website s3://derner-site
    aws cloudfront create-invalidation --distribution-id E2PRQSVYRFMT79 --paths '/*'