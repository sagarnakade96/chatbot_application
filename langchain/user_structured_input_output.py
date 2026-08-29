from dotenv import load_dotenv
from langchain_aws import ChatBedrockConverse
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from pydantic import BaseModel
from typing import Optional
class Student(BaseModel):
    name : str = 'Mirana'
    address :str = 'Pune'
    email : str
    phone_number : Optional[str] = None

student = Student(name="Sagar", email="Sagar.n@miranatoys.com", phone_number="123456789")
print(student)

