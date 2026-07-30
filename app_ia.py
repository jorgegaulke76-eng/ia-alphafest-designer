import streamlit as st
import io
from huggingface_hub import InferenceClient

st.set_page_config(page_title="IA Designer Alphafest", layout="centered")

st.title("🎨 Designer de IA - Alphafest")

# Barra lateral
hf_token = st.sidebar.text_input("Cole seu Token do Hugging Face (hf_...)", type="password")

# Campo de Upload (Voltou!)
uploaded_file = st.file_uploader("Enviar PDF ou Imagem de referência", type=["pdf", "png", "jpg"])

# Prompt
prompt = st.text_area("Descreva a arte que você deseja", "A beautiful sticker design for a party, high quality, vector style, white background")

if st.button("🚀 Gerar com IA"):
    if not hf_token:
        st.warning("Insira seu token do Hugging Face na barra lateral.")
    elif not hf_token.startswith("hf_"):
        st.error("Seu token parece inválido. Ele deve começar com 'hf_'.")
    else:
        with st.spinner("Conectando à IA..."):
            try:
                # Inicializa o cliente forçando o uso do token
                client = InferenceClient(model="runwayml/stable-diffusion-v1-5", token=hf_token)
                
                # Gera a imagem
                image = client.text_to_image(prompt)
                
                st.image(image, caption="Resultado Final")
                
                # Botão de Download
                buf = io.BytesIO()
                image.save(buf, format="PNG")
                st.download_button("📥 Baixar PNG", buf.getvalue(), "arte_alphafest.png", "image/png")
                
            except Exception as e:
                st.error("Erro na comunicação com a IA:")
                st.text(str(e))
                st.write("Verifique se o token copiado não tem espaços no início ou fim.")
