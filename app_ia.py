import streamlit as st
import io
from huggingface_hub import InferenceClient

st.set_page_config(page_title="IA Designer", layout="centered")
st.title("🎨 Designer de IA - Alphafest")

# Configuração simples
hf_token = st.sidebar.text_input("Cole seu Token do Hugging Face", type="password")
prompt = st.text_area("Descreva a arte", "A beautiful sticker design, high quality, white background")

if st.button("🚀 Gerar com IA"):
    if not hf_token:
        st.warning("Insira seu token na barra lateral.")
    else:
        with st.spinner("Conectando aos servidores da IA..."):
            try:
                # Instancia o cliente da forma padrão e recomendada
                client = InferenceClient(model="runwayml/stable-diffusion-v1-5", token=hf_token)
                
                # Gera a imagem
                image = client.text_to_image(prompt)
                
                st.image(image, caption="Resultado Final")
                
                # Download
                buf = io.BytesIO()
                image.save(buf, format="PNG")
                st.download_button("📥 Baixar PNG", buf.getvalue(), "arte.png", "image/png")
                
            except Exception as e:
                st.error("Erro na comunicação:")
                st.write("O servidor da IA pode estar temporariamente indisponível. Tente novamente em alguns segundos.")
                st.exception(e)
