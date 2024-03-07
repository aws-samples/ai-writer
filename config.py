AWS_REGION="us-west-2"
MODEL_ID="anthropic.claude-3-sonnet-20240229-v1:0"
MODEL_PARAMETERS={
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 4096,
    "temperature": 1.0,
}

## Example for Claude 2
# AWS_REGION="eu-central-1"
# MODEL_ID="anthropic.claude-v2"
# MODEL_PARAMETERS={
#     "max_tokens_to_sample": 2048,
#     "temperature": 1.0,
#     "top_k": 250,
#     "top_p": 1,
#     "stop_sequences": [ "\\n\\nHuman:" ],
#     "anthropic_version": "bedrock-2023-05-31"
# }
