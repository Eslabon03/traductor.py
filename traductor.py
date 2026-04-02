import streamlit as st
import pdfplumber
from deep_translator import GoogleTranslator
from gtts import gTTS
import io

# Control removido: la app es pública/personal por ahora
st.success("✅ Acceso Autorizado - Barmel Corp (Modo Personal)")

# Configuración de la App
st.title("Barmel Corporation: Intelligent Translator")
st.subheader("Herramienta Oficial de Traducción Técnica")
st.markdown("---")

# Tu lógica de traducción
col1, col2 = st.columns(2)
with col1:
    st.info("📂 Paso 1: Sube el manual o contrato en inglés")
    uploaded_file = st.file_uploader("", type=["pdf"])
    if uploaded_file and st.button("🚀 INICIAR TRADUCCIÓN"):
        with st.spinner("Procesando para Barmel Corp..."):
            with pdfplumber.open(uploaded_file) as pdf:
                texto_total = ""
                import textwrap
                translator = GoogleTranslator(source='en', target='es')
                for page in pdf.pages:
                    extract = page.extract_text()
                    if extract:
                        chunks = textwrap.wrap(extract, 4000, replace_whitespace=False)
                        for chunk in chunks:
                            try:
                                texto_total += translator.translate(chunk) + "\n"
                            except Exception as e:
                                st.error(f"Error de traducción: {e}")
                st.session_state.translated_text = texto_total
            st.success("✅ Traducción completada")

with col2:
    st.info("📝 Paso 2: Resultado y Audio")
    if 'translated_text' in st.session_state and st.session_state.translated_text:
        st.text_area("Texto en Español:", value=st.session_state.translated_text, height=250)
        if st.button("🔊 Escuchar"):
            tts = gTTS(text=st.session_state.translated_text, lang='es', tld='com.mx')
            buf = io.BytesIO()
            tts.write_to_fp(buf)
            st.audio(buf)

st.markdown("---")
st.caption("© 2026 Barmel Corporation | San Pedro Sula, Honduras. Uso exclusivo empresarial.")