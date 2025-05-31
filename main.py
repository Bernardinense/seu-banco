
import streamlit as st
import pandas as pd
import asyncio
import json
import os
from utils import imagem_para_base64


def load_css_com_imagem():
    base64_img = imagem_para_base64("assets/seta.jpg")

    with open(".streamlit/style.css", "r", encoding="utf-8") as f:
        css_template = f.read()

    css_com_imagem = css_template.replace("{{BASE64_IMAGE}}", base64_img)

    st.markdown(f"<style>{css_com_imagem}</style>", unsafe_allow_html=True)


# Importa as funções do seu core.py
from core import get_users_from_csv, gerar_sugestoes_ia, sugestoes_salvas

# --- Configurações da Página Streamlit ---
st.set_page_config(
    page_title="Consultor Financeiro AI - Seu Banco",
    page_icon="⭐", # Novo ícone para a aba do navegador, mais "atraente"
    layout="wide", # Mantém o layout amplo para espaço
    initial_sidebar_state="collapsed" # Começa com a barra lateral COLAPSADA
)
def load_css(file_name):
    """Carrega um arquivo CSS personalizado para estilizar o app."""
    with open(file_name, encoding="utf-8") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css_com_imagem()

st.markdown("""
<style>
div[data-testid="stContainer"] {
    background-color: rgba(255, 255, 255, 0.95) !important;
    border-radius: 15px !important;
    padding: 20px !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
    margin-bottom: 20px !important;
}
section[data-testid="stSidebar"] {
    background-color: #f0efdc !important;
    color: black;
    padding: 1rem;
    border-top-right-radius: 12px;
    border-bottom-right-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.dica-ia {
    background-color: rgba(30, 136, 229, 0.95); /* azul mais forte */
    padding: 20px;
    border-radius: 12px;
    color: white;
    font-size: 1.25em;
    font-weight: bold;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)


# --- Caminho do CSV ---
CSV_FILEPATH = "dados_bancarios_com_UserID.csv"

# --- Funções de Ajuda e Caching ---
@st.cache_data(show_spinner=False)
def load_data_from_csv():
    """Carrega os dados do CSV, com tratamento de erros."""
    try:
        df = pd.read_csv(CSV_FILEPATH)
        df.columns = df.columns.str.strip()
        return df
    except FileNotFoundError:
        st.error(f"Erro: O arquivo CSV não foi encontrado em '{CSV_FILEPATH}'. Por favor, verifique o caminho.")
        st.stop()
    except Exception as e:
        st.error(f"Erro ao carregar os dados do CSV: {e}")
        st.stop()

def generate_and_save_all_tips():
    """Gera e salva todas as dicas de IA no CSV, atualizando a interface."""
    st.info("Gerando e atualizando todas as dicas de IA. Isso pode levar alguns momentos...", icon="⏳")
    with st.spinner("Conectando-se à Inteligência Artificial e processando dados..."):
        try:
            sugestoes_dict = asyncio.run(gerar_sugestoes_ia(CSV_FILEPATH))
            sugestoes_salvas(CSV_FILEPATH, sugestoes_dict)
            st.success("Dicas de IA geradas e salvas com sucesso! ✨ Sua inteligência financeira está pronta!", icon="✅")
            st.cache_data.clear()
            st.rerun()
        except Exception as e:
            st.error(f"Ocorreu um erro ao gerar as dicas: {e}", icon="❌")
            st.warning("Por favor, verifique sua chave de API do Gemini, a conexão com a internet ou o formato do arquivo CSV.", icon="⚠️")


### 🌟 Seu Banco: Consultor Financeiro AI - A Nova Era das Finanças Pessoais 🌟

# --- Hero Section (Área de Destaque Inicial) ---
st.markdown("""
    <style>
    .big-font {
        font-size:3.5em !important;
        font-weight: bold;
        text-align: center;
        color: #1E88E5; /* Cor do seu primaryColor */
    }
    .medium-font {
        font-size:1.5em !important;
        text-align: center;
        color: #263238; /* Cor do seu textColor */
    }
    
    </style>
    <p class="big-font">💰 Seu Banco: Inteligência Financeira ao Seu Alcance 💰</p>
    <p class="medium-font">Transforme seus dados bancários em insights práticos e personalizados com o poder da Inteligência Artificial.</p>
    <br>
""", unsafe_allow_html=True)

# --- Mensagens de Status ---
col_status = st.container()

with col_status:
    df_all_users = load_data_from_csv()
    if 'SugestaoIA' not in df_all_users.columns or df_all_users['SugestaoIA'].isnull().any():
        st.warning("⚠️ Suas dicas de IA ainda não foram geradas ou estão incompletas. Clique no botão no menu ao lado para começar!", icon="⚠️")
    else:
        st.success("Dicas de IA prontas! Explore os insights personalizados para cada **Cliente**.", icon="✅")

st.markdown("---") # Separador visual

st.header("🧠 Explore Insights Personalizados")
st.markdown("⬅️***Selecione um Cliente na barra lateral para visualizar o perfil financeiro e a dica exclusiva da nossa Inteligência Artificial.***")

# --- Barra Lateral para Seleção e Ações ---
with st.sidebar:
    st.header("👤 Escolha o Cliente")
    st.markdown("---")

    # Mapeia o nome do usuário para seus dados completos para fácil acesso
    users_data = df_all_users.to_dict(orient='records')

    if not users_data:
        st.error("Nenhum usuário encontrado no arquivo CSV. Por favor, adicione dados e reinicie a aplicação.", icon="⚠️")
        st.stop()

    
    user_names = {user['name']: user for user in users_data}
    nome_opcoes = ["🔎 Selecione um Cliente..."] + list(user_names.keys())
    selected_name = st.selectbox("Selecione um cliente:", nome_opcoes, label_visibility="collapsed", key="cliente_selectbox")

    
    st.markdown("---")
    st.header("⚙️ Ações")

    if st.button("🚀 Gerar Todas as Dicas Agora!", use_container_width=True, help="Gera dicas para todos os Clientes"):
        generate_and_save_all_tips()

    st.markdown("---")
    st.info("*Implementação futura: enviar as sugestões por e-mail automaticamente para cada cliente.*", icon="📩")

    if st.button("📤 Disparar Sugestões", use_container_width=True, help="Envia de todas as dicas por e-mail para os clientes."):
        st.success("Disparo concluído! As sugestões foram enviadas por e-mail. (Futura Implementação)", icon="✅")


#Bloco Container

if selected_name != "🔎 Selecione um Cliente...":
    selected_user = user_names[selected_name]
    
    with st.container():
        
        # Conteúdo dentro do container
        st.subheader(f"📄 Perfil Financeiro de **{selected_user['name']}** (ID: {selected_user['UserID']})")

        st.markdown("##### Visão Geral:")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("💰 Saldo da Conta", f"R${selected_user['balance']:.2f}")
        with col2:
            st.metric("💳 Limite do Cartão", f"R${selected_user['card_limit']:.2f}")
        with col3:
            st.metric("🏦 Limite da Conta", f"R${selected_user['account_limit']:.2f}")

        st.markdown("---")

        st.subheader("💡 Dica Exclusiva da Inteligência Artificial:")

        sugestao = selected_user.get('SugestaoIA', None)
        if sugestao and pd.notna(sugestao):
            st.markdown(f'<div class="dica-ia">✨ {sugestao}</div>', unsafe_allow_html=True)
        else:
            st.warning("Dica de IA não disponível para este cliente. Por favor, gere as dicas usando o botão na barra lateral.", icon="⚠️")


st.markdown("---")
st.caption("2025 - Desenvolvido por Bruno Corrêa com Streamlit e Google Gemini AI. Uma iniciativa do **Seu Banco** para empoderar suas decisões financeiras.")    



