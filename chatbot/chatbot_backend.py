from langchain_classic.memory import ConversationSummaryBufferMemory
from langchain_classic.chains import ConversationChain
from langchain_aws import ChatBedrockConverse

def demo_chatbot() -> ChatBedrockConverse:
    demo_llm = ChatBedrockConverse(
        credentials_profile_name="develop-admin",
        model = "us.anthropic.claude-sonnet-4-5-20250929-v1:0",
        region_name="us-east-1",
        temperature=0.1,
        max_tokens=1000,
    )
    return demo_llm


def demo_memory() -> ConversationSummaryBufferMemory:
    llm_data = demo_chatbot()
    memory = ConversationSummaryBufferMemory(
        llm=llm_data,
        max_token_limit=1000,
    )
    return memory

def demo_conversation(input_text:str, memory: ConversationSummaryBufferMemory) -> str:
    llm_chain_data = demo_chatbot()
    llm_conversation = ConversationChain(
        llm=llm_chain_data,
        memory=memory,
        verbose=True,
    )
    chat_reply = llm_conversation.invoke(input_text)
    return chat_reply['response']


