import boto3
from dotenv import load_dotenv
load_dotenv()
import os
knowledge_base_id = os.getenv("KNOWLEDGE_BASE_ID")
bedrock_client = boto3.client(
    'bedrock-agent-runtime',
    region_name="us-east-1",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)
def invoke_bedrock_agent():
    try:
        user_prompt = "in the end from where signal is coming from to moon walker?"
        response = bedrock_client.agentic_retrieve_stream(
            messages=[
                {
                    "role": "user",
                    "content": {
                        "text": user_prompt
                    },
                }
            ],
            retrievers=[
                {
                    "description": "Moon Walker knowledge base",
                    "configuration": {
                        "knowledgeBase": {
                            "knowledgeBaseId": knowledge_base_id,
                            "retrievalOverrides": {
                                "maxNumberOfResults": 5
                            },
                        }
                    },
                }
            ],
            agenticRetrieveConfiguration={
                "foundationModelType": "MANAGED",
                "rerankingModelType": "MANAGED",
                "maxAgentIteration": 3,
            },
            generateResponse=True,
        )

        streamed_chunks = []
        final_answer = None

        error_event_names = {
            "accessDeniedException",
            "badGatewayException",
            "conflictException",
            "dependencyFailedException",
            "internalServerException",
            "resourceNotFoundException",
            "serviceQuotaExceededException",
            "throttlingException",
            "validationException",
        }

        for event in response["stream"]:
            # Partial answer streamed by AWS
            if "responseEvent" in event:
                text = event["responseEvent"].get("text", "")
                streamed_chunks.append(text)
                print(text, end="", flush=True)

            # Final answer, citations and retrieved results
            elif "result" in event:
                generated_response = event["result"].get(
                    "generatedResponse", {}
                )
                final_answer = generated_response.get("answer")

            else:
                for error_name in error_event_names:
                    if error_name in event:
                        message = event[error_name].get(
                            "message",
                            "Unknown streaming error",
                        )
                        raise RuntimeError(
                            f"{error_name}: {message}"
                        )

        print()

        # Prefer the final result; fall back to collected stream chunks.
        answer = final_answer or "".join(streamed_chunks)

        return {
            "statusCode": 200,
            "body": answer,
        }
                
        # print(client_knowledgebase)     
        #print(client_knowledgebase['output']['text'])
        #print(client_knowledgebase['citations'][0]['generatedResponsePart']['textResponsePart'])
        response_kbase_final=client_knowledgebase['output']['text']
        return {
            'statusCode': 200,
            'body': response_kbase_final
        }
    except Exception as e:
        print(f"Error occurred while invoking Bedrock agent: {e}")
        return None

result = invoke_bedrock_agent()