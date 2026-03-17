import streamlit as st
import pdfplumber
from deep_translator import GoogleTranslator
from gtts import gTTS
import io

# 1. ESTILO Y CONFIGURACIÓN DE MARCA
st.set_page_config(page_title="Barmel Translator Pro", page_icon="🎙️", layout="wide")

# CSS personalizado para colores de Barmel Corp (Azul empresarial y Gris profesional)
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button {
        background-color: #004a99;
        color: white;
        border-radius: 10px;
        height: 3em;
        width: 100%;
        font-weight: bold;
    }
    .stTitle { color: #004a99; font-family: 'Helvetica', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# Encabezado con Logo (Puedes cambiar la URL por la de tu logo real)
col1, col2 = st.columns([1, 5])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/3858/3858711.png", width=80) # Logo temporal
with col2:
    st.title("Barmel Corporation: Intelligent Translator")
    st.subheader("Herramienta Oficial de Traducción Técnica")

st.markdown("---")

# 2. LÓGICA DE LA APLICACIÓN
if 'translated_text' not in st.session_state:
    st.session_state.translated_text = ""

# Interfaz dividida en columnas
col_left, col_right = st.columns(2)

with col_left:
    st.info("📂 Paso 1: Sube el manual o contrato en inglés")
    uploaded_file = st.file_uploader("", type=["pdf"])
    
    if uploaded_file and st.button("🚀 INICIAR TRADUCCIÓN"):
        with st.spinner("Procesando para Barmel Corp..."):
            with pdfplumber.open(uploaded_file) as pdf:
                texto_total = ""
                for page in pdf.pages:
                    extract = page.extract_text()
                    if extract:
                        texto_total += GoogleTranslator(source='en', target='es').translate(extract) + "\n"
                st.session_state.translated_text = texto_total
            st.success("✅ Traducción completada con éxito")

with col_right:
    st.info("📝 Paso 2: Resultado y Audio")
    if st.session_state.translated_text:
        st.text_area("Texto en Español:", value=st.session_state.translated_text, height=250)
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔊 Escuchar"):
                tts = gTTS(text=st.session_state.translated_text, lang='es', tld='com.mx')
                buf = io.BytesIO()
                tts.write_to_fp(buf)
                st.audio(buf)
        with c2:
            st.download_button("📥 Descargar TXT", st.session_state.translated_text, "traduccion_barmel.txt")

# Pie de página legal
st.markdown("---")
st.caption("© 2026 Barmel Corporation | San Pedro Sula, Honduras. Uso exclusivo empresarial.")