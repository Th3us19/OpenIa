import openai
from dotenv import load_dotenv
import os
from colorama import Fore, Style, init
from datetime import datetime

load_dotenv()
client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))

#Inicializando o colorama
init(autoreset=True)


def geracao_texto(mensagens):
    resposta = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=mensagens,
        max_tokens=1000,
        temperature=0,
        stream=True
    )
    
    #Definindo a cor do texto do bot Fore.CYAN
    print(f"{Fore.CYAN}Bot: ", end="")
    texto_completo = ""
    for resposta_stream in resposta:
        texto = resposta_stream.choices[0].delta.content
        if texto:
            texto_completo += texto
            print(texto, end="")
    print()
    mensagens.append({"role": "assistant", "content": texto_completo})
    return mensagens

if __name__ == "__main__":
    print(f"{Fore.BLUE}Bem-vindo ao Chatboot 🤖")
    mensagens = [{
            "role": "system",
            "content": f"Você é um assistente útil. O ano atual é 2025. Hoje é {datetime.now().strftime('%d/%m/%Y')}."
        }]
    while True:
        # Definindo a cor do texto do usuário Fore.GREEN
        in_user = input(f"{Fore.GREEN}Usúario:")
        mensagens.append({"role": "user", "content": in_user})
        mensagens = geracao_texto(mensagens)