import pandas as pd
from dotenv import load_dotenv
import os
import asyncio
import json


load_dotenv()

api_key = os.getenv("API_KEY")
os.environ["GOOGLE_API_KEY"] = api_key

from google import genai


MODEL_ID = "gemini-2.0-flash"

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search
from google.genai import types


# Extract 

def get_users_from_csv(filepath):
    df = pd.read_csv(filepath)
    df.columns = df.columns.str.strip()
    return df.to_dict(orient='records')
    

def get_user_ids(filepath):
    df = pd.read_csv(filepath)
    df.columns = df.columns.str.strip()
    return df['UserID'].tolist()


# Transform

# Função Chama Agentes
async def call_agent(agent: Agent, message_text: str) -> str:
    session_service = InMemorySessionService()
    await session_service.create_session(app_name=agent.name, user_id="user1", session_id="session1")
    runner = Runner(agent=agent, app_name=agent.name, session_service=session_service)
    content = types.Content(role="user", parts=[types.Part(text=message_text)])

    final_response = ""
    async for event in runner.run_async(user_id="user1", session_id="session1", new_message=content):
        if event.is_final_response():
            for part in event.content.parts:
                if part.text:
                    final_response += part.text + "\n"
    return final_response.strip()

def criar_agente_dicas_financeiras():
    return Agent(
        name="agente_dicas_financeiras",
        model= MODEL_ID,
        instruction="""
Você é um especialista em finanças pessoais. Com base nos dados de nome, saldo da conta, limite da conta e limite do cartão, forneça uma dica financeira breve, prática e relevante para o usuário.
A dica deve ser personalizada e natural, mencionando apenas um dos dados financeiros (aquele mais relevante para o contexto da sugestão). Não repita todos os dados ou números exatos. Foque em gerar valor prático.
Use um tom amigável, encorajador e positivo. A resposta deve ter no máximo 500 caracteres.
No final da dica, adicione um emoji relacionado a progresso, motivação ou organização financeira, como por exemplo: 💡, 📈, ✅, 💪, 📊, 💰, 🧠, 🚀, 👌. Escolha aleatoriamente entre eles para manter as respostas variadas. Não use emojis no início ou meio da frase.
""",
        description="Gera dicas financeiras personalizadas",
         
       
    )

async def gerar_sugestoes_ia(caminho_csv):
    agente = criar_agente_dicas_financeiras()
    df = pd.read_csv(caminho_csv)
    df.columns = df.columns.str.strip()

    sugestoes_para_salvar = {}

    for index, row in df.iterrows():
        nome = row['name']
        saldo = row['balance']
        limite_conta = row['account_limit']
        limite_cartao = row['card_limit']
        user_id = row['UserID']

        prompt = (
            f"Nome: {nome}\n"
            f"Saldo da conta: R${saldo:.2f}\n"
            f"Limite da conta: R${limite_conta:.2f}\n"
            f"Limite do cartão: R${limite_cartao:.2f}\n\n"
            "Dê uma dica financeira útil, mostre os dados que voce utilizou na sugestão."
        )

        resposta = await call_agent(agente, prompt)  
        
        sugestoes_para_salvar[user_id] = resposta
        
        
    return sugestoes_para_salvar

def sugestoes_salvas(filepath, sugestoes_dict):
    df = pd.read_csv(filepath)
    df.columns = df.columns.str.strip()

    df['SugestaoIA'] = df['UserID'].map(sugestoes_dict)

    df['SugestaoIA'] = df['UserID'].apply(lambda x: sugestoes_dict.get(x, None))


    index = False
    df.to_csv(filepath, index=False)
    print(f'Sugestões salvas em: {filepath}')


if __name__ == "__main__":
    filepath = "dados_bancarios_com_UserID.csv"

    #Serve para testar localmente a função (quando necessário) 

    #print("User IDs:", get_user_ids(filepath))
    #print("Users data:")
    #print(json.dumps(get_users_from_csv(filepath), indent=2))

    print("\nLendo e processando dados do CSV para sugestões de IA...")
    sugestoes_dict = asyncio.run(gerar_sugestoes_ia(filepath))

    sugestoes_salvas(filepath, sugestoes_dict)

    print("\nSugestões geradas e salvas no CSV.\n")
    
    
    # Para teste de como estão saindo as sugestões(quando necessário)
    #for item in sugestoes:
    #    print(f"{item['Nome']}: {item['Sugestao']}")
