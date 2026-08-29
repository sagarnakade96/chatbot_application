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


st.header("Mirana Tool")
paper_input = st.selectbox( "Select Research Paper Name", ["Attention Is All You Need", "BERT: Pre-training of Deep Bidirectional Transformers", "GPT-3: Language Models are Few-Shot Learners", "Diffusion Models Beat GANs on Image Synthesis"] )

style_input = st.selectbox( "Select Explanation Style", ["Beginner-Friendly", "Technical", "Code-Oriented", "Mathematical"] ) 

length_input = st.selectbox( "Select Explanation Length", ["Short (1-2 paragraphs)", "Medium (3-5 paragraphs)", "Long (detailed explanation)"] )

template = load_prompt('template.json')
print(template)
if st.button("Summarize"):
    try:
        print(f"Invoking Model")
        chain = template | model
        print("Chain Formed")
        result = chain.invoke({
                    'paper_input':paper_input,
                    'style_input':style_input,
                    'length_input':length_input
                })
        print("Result Fetched")
        st.write(result.content)
    except Exception as e:
        print(f"{str(e)}")
        ValueError(str(e))