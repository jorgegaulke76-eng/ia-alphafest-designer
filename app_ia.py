import streamlit as st
import requests
import io
from PIL import Image

st.set_page_config(page_title="IA Designer Alphafest", layout="centered")

st.title("🎨 Designer de IA - Alphafest")

# Barra lateral
hf_token = st.sidebar.text_input("Cole seu Token do Hugging Face (Começa com hf_)", type="password")

# Campo de Upload
uploaded_file = st.file_uploader("Enviar PDF ou Imagem de referência", type=["pdf", "png", "jpg"])

# Prompt
prompt = st.text_area("Descreva a arte", "A beautiful sticker design, high quality, white background")

if st.button("🚀 Gerar com IA"):
    if not hf_token:
        st.warning("Insira seu token na barra lateral.")
    else:
        with st.spinner("Conectando direto ao servidor da IA..."):
            try:
                # API direta da Hugging Face
                API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
                headers = {"Authorization": f"Bearer {hf_token}"}
                
                payload = {"inputs": prompt}
                
                response = requests.post(API_URL, headers=headers, json=payload)
                
                if response.status_code == 200:
                    image = Image.open(io.BytesIO(response.content))
                    st.image(image, caption="Resultado Final")
                    
                    # Download
                    buf = io.BytesIO()
                    image.save(buf, format="PNG")
                    st.download_button("📥 Baixar PNG", buf.getvalue(), "arte.png", "image/png")
                else:
                    st.error(f"Erro na comunicação: Código {response.status_code}")
                    st.text(response.text)
                    
            except Exception as e:
                st.error("Erro técnico:")
                st.exception(e)
