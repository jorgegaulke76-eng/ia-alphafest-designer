import streamlit as st
import io
import os
from pdf2image import convert_from_bytes
from PIL import Image
from huggingface_hub import InferenceClient

st.set_page_config(page_title="IA Designer Alphafest", layout="centered")

st.title("🎨 IA Designer - Alphafest")
st.write("Transforme PDFs em artes A4 com IA (Na Nuvem).")

# Barra lateral para Token
hf_token = st.sidebar.text_input("Cole seu Token do Hugging Face", type="password")
prompt = st.text_area("Seu Prompt", "Transform the image into a high quality sticker design, vector style, white background")

def ajustar_para_a4(imagem):
    a4_size = (2480, 3508) # 300 DPI
    imagem.thumbnail(a4_size, Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", a4_size, "white")
    pos_x = (a4_size[0] - imagem.width) // 2
    pos_y = (a4_size[1] - imagem.height) // 2
    canvas.paste(imagem, (pos_x, pos_y))
    return canvas

uploaded_file = st.file_uploader("Envie o PDF", type=["pdf"])

if uploaded_file and prompt and hf_token:
    if st.button("🚀 Gerar com IA"):
        with st.spinner("Processando na nuvem..."):
            try:
                # O comando abaixo funciona na nuvem sem precisar de caminhos C:\
                images = convert_from_bytes(uploaded_file.getvalue())
                img_original = images[0]
                
                client = InferenceClient(model="runwayml/stable-diffusion-v1-5", token=hf_token)
                image_result = client.image_to_image(image=img_original, prompt=prompt)
                
                img_final = ajustar_para_a4(image_result)
                st.image(img_final, caption="Resultado Final")
                
                buf_out = io.BytesIO()
                img_final.save(buf_out, format="PNG", dpi=(300, 300))
                st.download_button("📥 Baixar PNG A4 (300 DPI)", buf_out.getvalue(), "arte_alphafest.png", "image/png")
            except Exception as e:
                st.error(f"Erro: {e}")
elif not hf_token:
    st.warning("Insira seu token do Hugging Face na barra lateral.")