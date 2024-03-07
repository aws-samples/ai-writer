import boto3
import json
import config

def invoke_llm(prompt):
    if config.MODEL_ID == 'anthropic.claude-3-sonnet-20240229-v1:0':
        return invoke_claude3sonnet(prompt)
    elif config.MODEL_ID == 'anthropic.claude-v2':
        return invoke_claude2(prompt)
    else:
        raise Exception("Invalid model")
    return None

def invoke_claude3sonnet(prompt):
    client = boto3.client('bedrock-runtime', region_name=config.AWS_REGION)

    try:
        response = client.invoke_model(
            body = json.dumps({
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ]
                    }
                ],
                **config.MODEL_PARAMETERS
            }),
            modelId = config.MODEL_ID,
            contentType = "application/json",
            accept = "application/json"
        )
        response_text = response['body'].read().decode('utf8').strip()
        response_json = json.loads(response_text)
        print(response_json)
        completion = response_json['content'][0]['text']
        return completion
    except Exception as e:
        print('Error invoking endpoint')
        print(e)
        raise Exception("Error invoking LLM. See Python CLI output for the full error message.")

def invoke_claude2(prompt):
    client = boto3.client('bedrock-runtime', region_name=config.AWS_REGION)

    claude2_prompt = f"""
Human: {prompt}

Assistant:"""

    try:
        response = client.invoke_model(
            body = bytes(json.dumps({
                "prompt": claude2_prompt,
                **config.MODEL_PARAMETERS
            }), 'utf-8'),
            modelId = config.MODEL_ID,
            contentType = "application/json",
            accept = "application/json"
        )
        response_text = response['body'].read().decode('utf8').strip()
        response_json = json.loads(response_text)
        completion = response_json['completion']
        return completion
    except Exception as e:
        print('Error invoking endpoint')
        print(e)
        raise Exception("Error invoking LLM")