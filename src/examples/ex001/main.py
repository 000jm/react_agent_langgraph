
from dotenv import load_dotenv
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

llm = ChatNVIDIA(model='nvidia/nemotron-3.5-lightning-30b-a3b')

response = llm.invoke([
    SystemMessage('traduza o seguinte do ingles pra o portugues'),
    HumanMessage('hello world')
])

print(response.content)
