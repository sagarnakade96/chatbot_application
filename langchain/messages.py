"""
system message
human messages
ai messages    
"""
from dotenv import load_dotenv
from langchain_aws import ChatBedrockConverse
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from pydantic import BaseModel

model = ChatBedrockConverse(
    credentials_profile_name="develop-admin",
    model = "us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    region_name="us-east-1",
    temperature=0.2,
    max_tokens=500,
)
load_dotenv()

messages = [
    SystemMessage(content="You are a intelligent AI assistant specially for programming and IT related things."),
    HumanMessage(content="Tell me about Redis and Langchain")
    
]

result = model.invoke(messages)

messages.append(result.content)

print(messages)
