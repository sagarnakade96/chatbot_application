import streamlit as st
from dotenv import load_dotenv
from langchain_aws import ChatBedrockConverse
load_dotenv()
import os
from langchain_aws import ChatBedrockConverse
from langchain_core.prompts import PromptTemplate,load_prompt
from langchain_core.load import loads, dumps

model = ChatBedrockConverse(
    credentials_profile_name="develop-admin",
    model = "us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    region_name="us-east-1",
    temperature=0.2,
    max_tokens=500,
)

chat_history = []

while True:
    user_input = input("You : ")
    if user_input == "Q" or user_input == "q":
        break
    chat_history.append(user_input)
    result = model.invoke(chat_history)
    llm_response = result.content
    chat_history.append(llm_response)
    print(f"AI : {llm_response}")

print(chat_history)