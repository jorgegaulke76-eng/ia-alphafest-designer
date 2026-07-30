import streamlit as st
import io
from huggingface_hub import InferenceClient

st.set_page_config(page_title="IA Designer Alphafest", layout="centered")
st.title("🎨 Designer de IA - Alphafest")

hf_token = st.sidebar.text_input("Cole seu Token do Hugging Face", type="password")
uploaded_file = st.file_uploader("Enviar PDF ou Imagem de referência", type=["pdf", "png", "jpg"])
prompt = st.text_area("Descreva a arte", "A beautiful sticker design, high quality, white background")

if st.button("🚀 Gerar com IA"):
    if not hf_token:
        st.warning("Insira seu token na barra lateral.")
    else:
        with st.spinner("Conectando..."):
            try:
                # Inicializa cliente corretamente
                client = InferenceClient(model="runwayml/stable-diffusion-v1-5", token=hf_token)
                
                # Gera imagem
                image = client.text_to_image(prompt)
                
                st.image(image, caption="Resultado Final")
                
                buf = io.BytesIO()
                image.save(buf, format="PNG")
                st.download_button("📥 Baixar PNG", buf.getvalue(), "arte.png", "image/png")
                
            except Exception as e:
                st.error("Erro:")
                st.exception(e)
                st.write("Dica: Se o erro for de conexão, aguarde alguns segundos e tente novamente.")
