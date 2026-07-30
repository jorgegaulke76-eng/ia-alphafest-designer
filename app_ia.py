import streamlit as st
import requests
import io
from PIL import Image
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

st.set_page_config(page_title="IA Designer", layout="centered")
st.title("🎨 Designer de IA - Alphafest")

hf_token = st.sidebar.text_input("Cole seu Token do Hugging Face", type="password")
uploaded_file = st.file_uploader("Envie sua imagem (PNG/JPG)", type=["png", "jpg", "jpeg"])
prompt = st.text_area("Descreva a arte", "A beautiful sticker design, high quality, white background")

if st.button("🚀 Transformar com IA"):
    if not hf_token or not uploaded_file:
        st.warning("Insira o token e envie uma imagem.")
    else:
        with st.spinner("Conectando (com repetição automática)..."):
            try:
                # Configuração de Repetição: se falhar, tenta 3 vezes
                session = requests.Session()
                retry = Retry(connect=3, backoff_factor=1)
                adapter = HTTPAdapter(max_retries=retry)
                session.mount('https://', adapter)

                API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
                headers = {"Authorization": f"Bearer {hf_token}"}
                files = {"image": uploaded_file.getvalue()}
                data = {"inputs": prompt}
                
                # Chamada com a sessão de repetição
                response = session.post(API_URL, headers=headers, files=files, timeout=60)
                
                if response.status_code == 200:
                    image = Image.open(io.BytesIO(response.content))
                    st.image(image, caption="Resultado Final")
                    
                    buf = io.BytesIO()
                    image.save(buf, format="PNG")
                    st.download_button("📥 Baixar PNG", buf.getvalue(), "arte.png", "image/png")
                else:
                    st.error(f"Erro {response.status_code}: {response.text}")
                    
            except Exception as e:
                st.error("Erro de conexão persistente na rede da Streamlit:")
                st.exception(e)
                st.write("Dica: Se este erro continuar, o Streamlit Cloud está com falha de DNS hoje.")
