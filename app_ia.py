import streamlit as st
import torch
from diffusers import StableDiffusionPipeline

st.set_page_config(page_title="IA Designer Alphafest", layout="centered")
st.title("🎨 Designer de IA - Alphafest")

# Carrega o modelo de forma simplificada
@st.cache_resource
def carregar_modelo():
    model_id = "runwayml/stable-diffusion-v1-5"
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float32)
    return pipe

prompt = st.text_area("Descreva a arte", "A high quality sticker design, white background")

if st.button("🚀 Gerar com IA"):
    with st.spinner("Gerando imagem... (pode demorar um pouco na primeira vez)"):
        try:
            pipe = carregar_modelo()
            image = pipe(prompt).images[0]
            st.image(image, caption="Resultado")
        except Exception as e:
            st.error("Erro interno:")
            st.exception(e)
