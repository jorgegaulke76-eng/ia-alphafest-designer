import streamlit as st
import requests
import io
from PIL import Image

st.set_page_config(page_title="IA Designer", layout="centered")
st.title("🎨 Designer de IA - Alphafest")

# Barra lateral
hf_token = st.sidebar.text_input("Cole seu Token do Hugging Face", type="password")
uploaded_file = st.file_uploader("Envie sua imagem (PNG/JPG)", type=["png", "jpg", "jpeg"])
prompt = st.text_area("Descreva a arte", "A beautiful 3D design, high quality, white background")

if st.button("🚀 Transformar com IA"):
    if not hf_token:
        st.warning("Insira o token.")
    elif not uploaded_file:
        st.warning("Envie uma imagem.")
    else:
        with st.spinner("Conectando..."):
            try:
                # 1. Preparar a imagem
                image_bytes = uploaded_file.getvalue()
                
                # 2. API Direta (sem biblioteca intermediária)
                API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
                headers = {"Authorization": f"Bearer {hf_token}"}
                
                # Envia a imagem como dados brutos
                response = requests.post(API_URL, headers=headers, data=image_bytes)
                
                if response.status_code == 200:
                    image = Image.open(io.BytesIO(response.content))
                    st.image(image, caption="Resultado Final")
                    
                    # Download
                    buf = io.BytesIO()
                    image.save(buf, format="PNG")
                    st.download_button("📥 Baixar PNG", buf.getvalue(), "arte.png", "image/png")
                else:
                    st.error(f"Erro {response.status_code}: {response.text}")
            except Exception as e:
                st.error("Erro técnico:")
                st.exception(e)
