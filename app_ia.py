import streamlit as st
import requests
import io
from PIL import Image

st.set_page_config(page_title="IA Designer Alphafest", layout="centered")
st.title("🎨 Designer de IA - Alphafest")

# Barra lateral para o Token
hf_token = st.sidebar.text_input("Cole seu Token do Hugging Face (hf_...)", type="password")

# Campo de upload de volta!
uploaded_file = st.file_uploader("Enviar Imagem (PNG/JPG)", type=["png", "jpg", "jpeg"])

# Prompt
prompt = st.text_area("Descreva a arte", "A beautiful sticker design, high quality, white background")

if st.button("🚀 Gerar com IA"):
    if not hf_token:
        st.warning("Insira o token na barra lateral.")
    elif not uploaded_file:
        st.warning("Por favor, envie uma imagem.")
    else:
        with st.spinner("Conectando..."):
            try:
                # API Direta (mais leve e menos propensa a erros)
                API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
                headers = {"Authorization": f"Bearer {hf_token}"}
                
                # Envia a imagem e o prompt
                files = {"image": uploaded_file.getvalue()}
                data = {"inputs": prompt}
                
                response = requests.post(API_URL, headers=headers, files=files)
                
                if response.status_code == 200:
                    image = Image.open(io.BytesIO(response.content))
                    st.image(image, caption="Resultado Final")
                    
                    buf = io.BytesIO()
                    image.save(buf, format="PNG")
                    st.download_button("📥 Baixar PNG", buf.getvalue(), "arte.png", "image/png")
                else:
                    st.error(f"Erro {response.status_code}: {response.text}")
                    st.write("Dica: Se o erro persistir, tente novamente em 30 segundos.")
                    
            except Exception as e:
                st.error("Erro técnico na rede:")
                st.exception(e)
