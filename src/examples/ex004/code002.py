
import threading
from dotenv import load_dotenv

from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langgraph.graph import END, START, StateGraph, add_messages
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage

from typing import Annotated, Sequence, TypedDict

from langgraph.graph.message import Messages
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.state import RunnableConfig

load_dotenv()

llm = ChatNVIDIA(model='nvidia/nemotron-3.5-lightning-30b-a3b')

# 1 - Definir o state
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

# 2 - Definir os nodes
def call_llm(state: AgentState) -> AgentState:
    llm_result = llm.invoke(state['messages'])
    return {'messages': [llm_result]}

# 3 - Criar o builder
builder = StateGraph(state_schema=AgentState, context_schema=None, input_schema=AgentState, output_schema=AgentState)

# 4 - Adicionar nodes ao grafo
builder.add_node('call_llm', call_llm)

# 4 - Adicionar edges ao grafo
builder.add_edge(START, 'call_llm')
builder.add_edge('call_llm', END)

# 5 - Compilar o graph
checkpointer = InMemorySaver
graph = builder.compile(checkpointer)
config = RunnableConfig(configurable={'thread_id': threading.get_ident()})

if __name__ == '__main__':
    # 6 - Usar o graph
    while True:
        user_input = input('Digite sua mensagem: ')

        if (user_input.lower()) in ['exit', 'q', 'quit']:
            break

        human_message = HumanMessage(user_input)
        result = graph.invoke({'messages': human_message}, config)

        print(str(result['messages'][-1].content))

