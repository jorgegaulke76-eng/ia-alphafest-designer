import streamlit as st
import io
import traceback
from huggingface_hub import InferenceClient

st.set_page_config(page_title="IA Designer Alphafest", layout="centered")

st.title("🎨 Designer de IA - Alphafest")

# Barra lateral
hf_token = st.sidebar.text_input("Cole seu Token do Hugging Face", type="password")

# Campo de Upload (VOLTOU!)
uploaded_file = st.file_uploader("Enviar PDF ou Imagem de referência", type=["pdf", "png", "jpg"])

# Prompt
prompt = st.text_area("Descreva a arte", "A beautiful sticker design for a party, vector style, white background")

if st.button("🚀 Gerar com IA"):
    if not hf_token:
        st.warning("Insira seu token na barra lateral.")
    else:
        with st.spinner("Conectando à IA..."):
            try:
                # Inicializa o cliente
                client = InferenceClient(token=hf_token)
                
                # Gerar imagem forçando o modelo dentro da função (isso evita o erro StopIteration)
                image = client.text_to_image(
                    prompt, 
                    model="runwayml/stable-diffusion-v1-5"
                )
                
                st.image(image, caption="Resultado Final")
                
                # Download
                buf = io.BytesIO()
                image.save(buf, format="PNG")
                st.download_button("📥 Baixar PNG", buf.getvalue(), "arte.png", "image/png")
                
            except Exception as e:
                st.error("Erro na comunicação com a IA:")
                st.text("Detalhes do erro:")
                st.text(str(e))
                st.write("Dica: Se o erro persistir, o servidor gratuito da Hugging Face pode estar temporariamente ocupado.")
