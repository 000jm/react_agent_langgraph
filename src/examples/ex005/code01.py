
from dotenv import load_dotenv

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.outputs import llm_result
from langchain_core.tools import BaseTool, tool
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from pydantic import ValidationError

from rich import print

load_dotenv()

llm = ChatNVIDIA(model='nvidia/nemotron-3.5-lightning-30b-a3b')

# 1 - Criar as ferramentas
@tool
def multiply(a: int, b: int) -> int:
    """
    Multiply a * b and returns the result

    Args:
        a: int multiplicand
        b: multiplier

    Returns:
        the resulting int of the equation a * b
    """
    return a * b

# result = multiply.invoke({'a': 6, 'b': 2})

# print(result)

system_message = SystemMessage(
    'You are a helpful assistant. You have acess to tools. When the user asks'
    'for something, first look if you have a tool that solves that problem.'
)
user_input = input('Digite sua mensagem: ')
human_message = HumanMessage(user_input)
messages: list[BaseMessage] = [system_message, human_message]

result = llm.invoke(messages)

tools: list[BaseTool] = [multiply]
tools_by_name = {tool.name: tool for tool in tools}
llm_with_tools = llm.bind_tools(tools)

llm_response = llm_with_tools.invoke(messages)
messages.append(llm_response)

if isinstance(llm_response, AIMessage) and getattr(llm_response, 'tool_calls', None):
    call = llm_response.tool_calls[-1]
    name, args, id_ = call['name'], call['args'], call['id']

    try:
        content = tools_by_name[name].invoke(args)
        status = 'success'
    except(KeyError, IndexError, TypeError, ValidationError, ValueError) as error:
        content = f'Please, fix your mistakes: {error}'
        status = 'error'

    tool_message = ToolMessage(content=content, tool_call_id=id_, status=status)
    messages.append(tool_message)

    llm_response = llm_with_tools.invoke(messages)
    messages.append(llm_response)
