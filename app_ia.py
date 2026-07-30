import streamlit as st
import io
from huggingface_hub import InferenceClient

st.set_page_config(page_title="IA Designer Alphafest", layout="centered")

st.title("🎨 Designer de IA - Alphafest")

# Barra lateral
hf_token = st.sidebar.text_input("Cole seu Token do Hugging Face", type="password")

# Campo de Upload (Mantido)
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
                # O SEGREDO ESTÁ AQUI: Definimos o modelo no início
                client = InferenceClient(model="stabilityai/sd-turbo", token=hf_token)
                
                # Chamada direta e limpa
                image = client.text_to_image(prompt)
                
                st.image(image, caption="Resultado Final")
                
                # Download
                buf = io.BytesIO()
                image.save(buf, format="PNG")
                st.download_button("📥 Baixar PNG", buf.getvalue(), "arte.png", "image/png")
                
            except Exception as e:
                st.error("Erro técnico:")
                st.exception(e)
