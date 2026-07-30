import streamlit as st
import io
import traceback
from huggingface_hub import InferenceClient

st.set_page_config(page_title="IA Designer Alphafest", layout="centered")

st.title("🎨 Designer de IA - Alphafest")

# Configuração
hf_token = st.sidebar.text_input("Cole seu Token do Hugging Face (Começa com hf_)", type="password")
prompt = st.text_area("Descreva a arte", "A beautiful sticker design for a party, vector style, white background")

if st.button("🚀 Gerar com IA"):
    if not hf_token:
        st.warning("Insira seu token na barra lateral.")
    else:
        with st.spinner("Conectando à IA..."):
            try:
                # Inicializa o cliente
                client = InferenceClient(model="runwayml/stable-diffusion-v1-5", token=hf_token)
                
                # Teste simples de geração
                image = client.text_to_image(prompt)
                
                st.image(image, caption="Resultado Final")
                
                # Download
                buf = io.BytesIO()
                image.save(buf, format="PNG")
                st.download_button("📥 Baixar PNG", buf.getvalue(), "arte.png", "image/png")
                
            except Exception as e:
                # ISSO VAI MOSTRAR O ERRO REAL NA TELA
                st.error("Erro na comunicação com a IA:")
                st.text(str(e))
                st.subheader("Detalhes Técnicos (O que está travando):")
                st.code(traceback.format_exc())
