import json
import os

from boto3 import client
from dotenv import load_dotenv

load_dotenv()

agent_client = client(
    "bedrock-runtime",
    region_name="us-east-1",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)
model_id = "amazon.nova-pro-v1:0"
inference_config = {
    "maxTokens": 2500,
    "temperature": 0.7,
    "topP": 0.9,
    "topK": 20,
}
system_prompt = [
    {
        "text": "Act as a wind turbine manufacturing assistant. Your main task is to summarize the logs in 5 lines. "
        "Make the logs understandable for a non-technical person. If the logs contain any errors, please highlight them in your summary. "
        "If the logs are too long, please summarize them in a concise manner."
    }
]


def invoke_agent(user_input):
    message_prompt = [
        {
            "role": "user",
            "content": [{"text": user_input}],
        }
    ]
    body_request = {
        "schemaVersion": "messages-v1",
        "messages": message_prompt,
        "system": system_prompt,
        "inferenceConfig": inference_config,
    }

    response = agent_client.invoke_model(
        modelId=model_id,
        contentType="application/json",
        accept="application/json",
        body=json.dumps(body_request),
        trace="ENABLED",
        guardrailIdentifier="myjz44g4d0n7",
        guardrailVersion='1',
        performanceConfigLatency="standard",
    )

    response_status_code = response["ResponseMetadata"]["HTTPStatusCode"]
    if response_status_code != 200:
        return response_status_code, None

    response_body = json.loads(response["body"].read())
    print(f"fetch response status code: {response_body}")
    final_response = response_body["output"]["message"]["content"][0]["text"]
    return response_status_code, final_response
