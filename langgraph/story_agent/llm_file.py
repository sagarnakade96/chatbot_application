from langchain_aws import ChatBedrockConverse
from langchain_core.messages import AIMessage, HumanMessage
from IPython.display import Image, display
from pprint import pprint
import os
from dotenv import load_dotenv
load_dotenv() 
llm = ChatBedrockConverse(
        credentials_profile_name="develop-admin",
        model = "us.anthropic.claude-sonnet-4-5-20250929-v1:0",
        region_name="us-east-1",
        temperature=0.1,
        max_tokens=500,
    )
