import streamlit as st
from huggingface_hub import InferenceClient

st.set_page_config(page_title="IA Designer Alphafest", layout="centered")

st.title("🎨 Designer de IA - Alphafest")

# Barra lateral
hf_token = st.sidebar.text_input("Cole seu Token do Hugging Face", type="password")

# Campo de Upload
uploaded_file = st.file_uploader("Enviar PDF ou Imagem de referência", type=["pdf", "png", "jpg"])

# Prompt
prompt = st.text_area("Descreva a arte", "A beautiful sticker design, high quality, white background")

if st.button("🚀 Gerar com IA"):
    if not hf_token:
        st.warning("Insira seu token na barra lateral.")
    elif not hf_token.startswith("hf_"):
        st.error("O token deve começar com 'hf_'")
    else:
        with st.spinner("Conectando..."):
            try:
                # Usando o modelo SD-Turbo (mais estável para conta gratuita)
                client = InferenceClient(token=hf_token)
                image = client.text_to_image(
                    prompt, 
                    model="stabilityai/sd-turbo"
                )
                
                st.image(image, caption="Resultado Final")
                
            except Exception as e:
                st.error("Erro na comunicação com a IA:")
                # ISSO VAI MOSTRAR O ERRO REAL NA TELA
                st.exception(e)
                st.write("Dica: Se aparecer '401', seu Token está incorreto ou sem permissão.")
                st.write("Dica: Se aparecer '429', você estourou o limite de uso gratuito hoje.")
