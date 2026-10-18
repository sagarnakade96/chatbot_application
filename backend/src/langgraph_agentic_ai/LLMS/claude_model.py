from dotenv import load_dotenv
from langchain_aws import ChatBedrockConverse
load_dotenv()
from langchain_aws import ChatBedrockConverse

model = ChatBedrockConverse(
    credentials_profile_name="develop-admin",
    model = "us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    region_name="us-east-1",
    temperature=0.2,
    max_tokens=500,
)
