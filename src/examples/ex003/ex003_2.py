
from dataclasses import dataclass
from typing import Annotated, Literal
from langgraph.graph import START, END, StateGraph, add_messages
import operator

# 1 - Definir o estado
@dataclass
class State:
    nodes_path: Annotated[list[str], operator.add]
    current_number: int = 0

# 2 - Criar os nodes
def node_a(state: State) -> State:
    output_state: State = State(nodes_path=['node_a'], current_number=22)
    print('> node_a', f"{state}")
    return output_state

def node_b(state: State) -> State:
    output_state: State = State(nodes_path=['node_b'], current_number=67)
    print('> node_b', f"{state}", f"{output_state}")
    return output_state

def node_c(state: State) -> State:
    output_state: State = State(nodes_path=['node_c'], current_number=22)
    print('> node_c', f"{state}", f"{output_state}")
    return output_state

def the_condicional(state: State) -> Literal['goes_to_b', 'goes_to_c']:
    if state.current_number >= 50:
        return 'goes_to_c'

    return 'goes_to_b'

# Definir o builder do grafo
builder = StateGraph(State)

# Adicionar os nodes
builder.add_node('node_a', node_a)
builder.add_node('node_b', node_b)
builder.add_node('node_c', node_c)

# Conectar os nodes usando as edges(arestas)
builder.add_edge(START, 'node_a')
# builder.add_conditional_edges('node_a', the_condicional, ['node_b', 'node_c'])
# builder.add_conditional_edges('node_a', the_condicional, {
#     'node_b': 'node_b',
#     'node_b': 'node_c'
# })
builder.add_conditional_edges('node_a', the_condicional, {
    'goes_to_b': 'node_b',
    'goes_to_c': 'node_c'
})
builder.add_edge('node_b', END)
builder.add_edge('node_c', END)

# Compilar o grafo
graph = builder.compile()

graph.get_graph().draw_mermaid_png(output_file_path='graph.png')

response = graph.invoke(State(nodes_path=[], current_number=67))

print(response)
