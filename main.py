import streamlit as st
import requests
import os

BACKEND_URL = "https://orac-bot.onrender.com/orac-ia"

SENHA_ORAC_IA = os.getenv('SENHA_ORAC_IA')

st.set_page_config(page_title="Orac IA",
                   page_icon="assets/orac.png", layout="wide")

col_image, col_title = st.columns(
    [1, 12], gap=None, vertical_alignment='center')
with col_image:
    st.image("assets/orac.png", width=100)
with col_title:
    st.title("Orac IA")

col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    nome_usuario = st.text_input("Seu nome")
with col2:
    email = st.text_input("Seu e-mail")
with col3:
    arquivo = st.file_uploader("Anexar documento", type=["pdf"])

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

if prompt := st.chat_input("Digite sua mensagem..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt, unsafe_allow_html=True)

    data = {
        "nome_usuario": nome_usuario,
        "email": email,
        "mensagem": prompt,
        "senha": SENHA_ORAC_IA
    }
    files = {"arquivo": (arquivo.name, arquivo,
                         arquivo.type)} if arquivo else None

    try:
        response = requests.post(BACKEND_URL, data=data, files=files)
        if response.status_code == 200:
            resposta = response.json().get("resposta", {})
            output = resposta.get(
                "output", "⚠️ Nenhuma resposta recebida.")
        else:
            output = f"⚠️ Erro {response.status_code}: {response.json().get('erro', response.text)}"
    except Exception as e:
        output = f"❌ Erro de conexão: {e}"

    st.session_state.messages.append(
        {"role": "assistant", "content": output})
    st.chat_message("assistant").markdown(output, unsafe_allow_html=True)
