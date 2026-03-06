import boto3
import json

client = boto3.client('bedrock-runtime', region_name="us-east-1")

accept = 'application/json'
contentType = 'application/json'

response = client.invoke_model(
    accept=accept, 
    contentType=contentType,
    modelId="arn:aws:bedrock:us-east-1:842675989330:inference-profile/us.anthropic.claude-sonnet-4-6",
    body=json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 2000,
        "messages": [
            {
                "role": "user",
                "content": "Explain what AWS Bedrock is"
            }
        ]
    })
)

response_body = json.loads(response.get('body').read())
print(response_body['content'][0]['text'])


