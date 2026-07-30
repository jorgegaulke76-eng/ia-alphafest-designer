import streamlit as st
import io
import traceback
from pdf2image import convert_from_bytes
from PIL import Image
from huggingface_hub import InferenceClient

st.set_page_config(page_title="IA Designer Alphafest", layout="centered")

st.title("🎨 Designer de IA - Alphafest")
st.write("Transforme PDFs em artes A4 com IA.")

hf_token = st.sidebar.text_input("Cole seu Token do Hugging Face", type="password")
prompt = st.text_area("Seu Prompt", "Transform the image into a high quality sticker design, vector style, white background")

uploaded_file = st.file_uploader("Enviar PDF", type=["pdf"])

if uploaded_file and prompt and hf_token:
    if st.button("🚀 Gerar com IA"):
        with st.spinner("Processando na nuvem..."):
            try:
                # 1. Converter PDF
                images = convert_from_bytes(uploaded_file.getvalue())
                img_original = images[0]
                
                # 2. Conectar e Gerar
                client = InferenceClient(model="runwayml/stable-diffusion-v1-5", token=hf_token)
                
                # Vamos tentar a geração
                image_result = client.image_to_image(image=img_original, prompt=prompt)
                
                # 3. Ajustar e Exibir
                st.image(image_result, caption="Resultado Final")
                
            except Exception as e:
                st.error("Ops! Ocorreu um erro técnico:")
                st.text(str(e))
                st.text("Detalhes do erro:")
                st.text(traceback.format_exc())

elif not hf_token:
    st.warning("Insira seu token do Hugging Face na barra lateral.")
