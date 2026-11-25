

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_nvidia_ai_endpoints import ChatNVIDIA

load_dotenv()

llm = ChatNVIDIA(model='nvidia/nemotron-3.5-lightning-30b-a3b')

system_message = SystemMessage(
    "Você é um guia de estudos que ajuda estudantes a aprenderem novos tópicos. \n\n"
    "Seu trabalho é guiar as ideias do estudante para que ele consiga entender o "
    "tópico escolhido sem receber respostas prontas da sua parte. \n\n"
    "Evite conversar sobre assuntos paralelos ao tópico escolhido. Se o estudante "
    "não fornecer um tópico inicialmente, seu primeiro trabalho será solicitar um "
    "tópico até que o estudante o informe. \n\n"
    "Você pode ser amigável, descolado e tratar o estudante como adolescente. Queremos "
    "evitar a fadiga de um estudo rígido e mantê-lo engajado no que estiver "
    "estudando. \n\n"
    "As próximas mensagens serão de um estudante. "
)

human_message = HumanMessage("Olá, meu nome é João Miguel")

messages = [system_message, human_message]
response = llm.invoke(messages)
print(f"{'AI':-^80}")
print(response.content)

messages.append(response)
while True:
    print(f"{'Human':-^80}")
    user_input = input('Digite sua mensagem: ')
    human_message = HumanMessage(user_input)

    if (user_input.lower()) in ['exit', 'q']:
        break

    messages.append(human_message)

    response = llm.invoke(messages)

    print(f"{'AI':-^80}")
    print(response.content)

    messages.append(response)

print()
print(f"{'Histórico':-^80}")
print(*[f"{m.type.upper()}\n{m.content}\n\n" for m in messages], sep='', end='')
print()
