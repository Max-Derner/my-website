# tells you what recipes are available
tell-me:
    just --list


# deploys the infra structure required to host the website
deploy-infra:
    cdk deploy --all --outputs-file outputs.json


# pushes the website to the prepared infrastructure
publish-site:
    aws s3 sync ./website s3://"$(jq -r .DernerWebsite.bucket outputs.json)"
    aws cloudfront create-invalidation --distribution-id "$(jq -r .DernerWebsite.distid outputs.json)" --paths '/*'
