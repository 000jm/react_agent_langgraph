
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, add_messages
import operator

# def reducer(a: list[str], b: list[str]) -> list[str]:
#     return a + b

# 1 - Definir o estado
class State(TypedDict):
    nodes_path: list[str]
    # nodes_path: Annotated[list[str], reducer]
    nodes_path: Annotated[list[str], operator.add]
    # nodes_path: Annotated[list[str], add_messages]

# 2 - Criar os nodes
def node_a(state: State) -> State:
    output_state: State = {'nodes_path': ['node_a']}
    print('> node_a', f"{output_state}")
    return output_state

def node_b(state: State) -> State:
    output_state: State = {'nodes_path': ['node_b']}
    print('> node_b', f"{state}", f"{output_state}")
    return output_state

# Definir o builder do grafo
builder = StateGraph(State)

# Adicionar os nodes
builder.add_node('node_a', node_a)
builder.add_node('node_b', node_b)

# Conectar os nodes usando as edges(arestas)
builder.add_edge('__start__', 'node_a')
builder.add_edge('node_a', 'node_b')
builder.add_edge('node_b', '__end__')

# Compilar o grafo
graph = builder.compile()

graph.get_graph().draw_mermaid_png(output_file_path='graph.png')

response = graph.invoke(State([]))

print(response)
