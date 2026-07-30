import streamlit as st
import io
import traceback
from huggingface_hub import InferenceClient

st.set_page_config(page_title="IA Designer Alphafest", layout="centered")

st.title("🎨 Designer de IA - Alphafest")
st.write("Gerador de imagens via IA (Nuvem).")

# Barra lateral
hf_token = st.sidebar.text_input("Cole seu Token do Hugging Face", type="password")

# Prompt
prompt = st.text_area("Descreva a arte que você deseja", "A beautiful sticker design for a party, high quality, vector style, white background")

if st.button("🚀 Gerar Imagem com IA"):
    if not hf_token:
        st.warning("Insira seu token do Hugging Face na barra lateral.")
    else:
        with st.spinner("Conectando à IA..."):
            try:
                # Usando um cliente genérico
                client = InferenceClient(token=hf_token)
                
                # Vamos usar um modelo clássico e liberado: 'runwayml/stable-diffusion-v1-5'
                # Usando text-to-image, que é a função que o plano gratuito aceita
                image = client.text_to_image(prompt, model="runwayml/stable-diffusion-v1-5")
                
                st.image(image, caption="Resultado Final")
                
                # Botão de Download
                buf = io.BytesIO()
                image.save(buf, format="PNG")
                st.download_button("📥 Baixar PNG", buf.getvalue(), "arte_alphafest.png", "image/png")
                
            except Exception as e:
                st.error("Erro na comunicação com a IA:")
                st.text(str(e))
                st.write("Nota: Se aparecer '401', verifique se o seu token tem permissão de leitura.")
