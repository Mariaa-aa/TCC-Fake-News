# chat_ia.py

import openai
import time
import os  # módulo os para acessar variáveis de ambiente
from dotenv import load_dotenv # load_dotenv carrega variáveis de um arquivo .env


from UOL import get_news

load_dotenv() # procurar por um arquivo .env 

openai.api_key = os.getenv("OPENAI_API_KEY")

# Verifica se a chave foi carregada. Se não, avisa e encerra.
if not openai.api_key:
    print("ERRO: A chave de API da OpenAI (OPENAI_API_KEY) não foi encontrada nas variáveis de ambiente.")
    print("Por favor, crie um arquivo .env na raiz do seu projeto com 'OPENAI_API_KEY=sua_chave_aqui'")
    print("Ou defina a variável de ambiente OPENAI_API_KEY no seu sistema.")
    exit()

print(
    f"DEBUG: Chave de API configurada (primeiros 5 caracteres): {openai.api_key[:5]}*****")

############

def obter_resumo_chatgpt(manchete_text):
    print(
        f"DEBUG: Tentando obter fake news para a manchete: '{manchete_text}'")
    try:
            response = openai.chat.completions.create(
             model="gpt-3.5-turbo",
             messages=[
                 {
                 "role": "system",
                     "content": "Você é um gerador de notícias alternativas e controversas. Sua tarefa é criar uma manchete FALSA e CHAMATIVA, que contradiga ou distorça o sentido da manchete original, sem que pareça obviamente falsa. Não revele que é uma fake news. Seja criativo na desinformação."
                 },
                 {
                     "role": "user",
                     "content": f"Crie uma manchete falsa que contradiga ou distorça a seguinte manchete verdadeira: '{manchete_text}'"
                 }
             ],
             max_tokens=50,
             temperature=0.8
        )

            fake_news_gerada = response.choices[0].message.content.strip()
            print(f"DEBUG: ChatGPT gerou: '{fake_news_gerada}'")

            time.sleep(1)  # Pausa de 1 segundo para evitar sobrecarga

            return fake_news_gerada
    except openai.APIError as e:
            print(f"DEBUG: Erro na API do OpenAI ao processar '{manchete_text}': {e}")
            return None
    except Exception as e:
            print(f"DEBUG: Erro inesperado ao processar '{manchete_text}': {e}")
            return None


if __name__ == "__main__":
    print("Iniciando a coleta de notícias do UOL...")
    manchetes = get_news()

    if manchetes:
        print(f"\n{len(manchetes)} Manchetes encontradas. Processando com ChatGPT...\n")

        for i, item_manchete in enumerate(manchetes): # Processa até 5 manchetes

            try:
                titulo = item_manchete.get('titulo', item_manchete.text.strip())

            except AttributeError:
                titulo = str(item_manchete)

            if len(titulo) < 30:
                continue

            print(f"--- Processando Manchete {i+1} ---")
            print(f"Manchete Original: {titulo}")

            fake_news = obter_resumo_chatgpt(titulo)

            if fake_news:
                print(f"Fake News Gerada: {fake_news}\n")
            else:
                print("Não foi possível gerar a Fake News para esta manchete.\n")
    else:
        print("Nenhuma manchete encontrada pelo UOL.py.")