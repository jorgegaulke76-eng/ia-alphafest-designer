import streamlit as st
import io
from PIL import Image
from huggingface_hub import InferenceClient

st.set_page_config(page_title="IA Designer", layout="centered")
st.title("🎨 Designer de IA - Alphafest")

# Configuração
hf_token = st.sidebar.text_input("Cole seu Token do Hugging Face", type="password")

# Campo de Upload apenas para Imagens (muito mais leve)
uploaded_file = st.file_uploader("Envie sua imagem de referência (PNG ou JPG)", type=["png", "jpg", "jpeg"])

# Prompt
prompt = st.text_area(
    "Descreva a arte", 
    "Transforme em um design 3D de alta qualidade, cores vibrantes, fundo branco, estilo vetor realista"
)

if st.button("🚀 Transformar com IA"):
    if not hf_token:
        st.warning("Insira o token na barra lateral.")
    elif not uploaded_file:
        st.warning("Por favor, anexe uma imagem antes de gerar.")
    else:
        with st.spinner("Enviando e processando na IA..."):
            try:
                # 1. Abrir a imagem que você enviou
                img_original = Image.open(uploaded_file).convert("RGB")
                
                # 2. Truque de mestre: Redimensionar para o limite do plano gratuito (512x512)
                img_original.thumbnail((512, 512))
                
                # 3. Conectar à IA
                client = InferenceClient(model="runwayml/stable-diffusion-v1-5", token=hf_token)
                
                # 4. Transformar a imagem
                image_result = client.image_to_image(image=img_original, prompt=prompt)
                
                # 5. Mostrar na tela
                st.image(image_result, caption="Sua nova arte gerada!")
                
                # 6. Preparar para baixar
                buf = io.BytesIO()
                image_result.save(buf, format="PNG")
                st.download_button("📥 Baixar Arte em PNG", buf.getvalue(), "arte_alphafest.png", "image/png")
                
            except Exception as e:
                st.error("Ocorreu um erro técnico na nuvem:")
                st.exception(e)
                st.write("Dica: Se for erro de conexão, aguarde 30 segundos e tente novamente.")
