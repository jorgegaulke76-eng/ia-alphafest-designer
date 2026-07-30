import streamlit as st
import requests
import io
from PIL import Image

st.set_page_config(page_title="IA Designer", layout="centered")
st.title("🎨 Designer de IA - Alphafest")

hf_token = st.sidebar.text_input("Cole seu Token do Hugging Face", type="password")
uploaded_file = st.file_uploader("Enviar PDF ou Imagem", type=["pdf", "png", "jpg"])
prompt = st.text_area("Descreva a arte", "A beautiful sticker design, high quality, white background")

if st.button("🚀 Gerar com IA"):
    if not hf_token:
        st.warning("Insira o token.")
    else:
        with st.spinner("Gerando..."):
            try:
                # Conexão direta (sem biblioteca intermediária)
                url = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
                headers = {"Authorization": f"Bearer {hf_token}"}
                payload = {"inputs": prompt}
                
                response = requests.post(url, headers=headers, json=payload)
                
                if response.status_code == 200:
                    image = Image.open(io.BytesIO(response.content))
                    st.image(image, caption="Resultado Final")
                    
                    buf = io.BytesIO()
                    image.save(buf, format="PNG")
                    st.download_button("📥 Baixar PNG", buf.getvalue(), "arte.png", "image/png")
                else:
                    st.error(f"Erro {response.status_code}: {response.text}")
                    
            except Exception as e:
                st.error("Erro técnico:")
                st.exception(e)
