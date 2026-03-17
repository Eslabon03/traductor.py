import streamlit as st
import pdfplumber
from deep_translator import GoogleTranslator
from gtts import gTTS
import io

# --- 1. FUNCIÓN DE SEGURIDAD ---
def check_password():
    def password_entered():
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"] 
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.image("https://cdn-icons-png.flaticon.com/512/2592/2592231.png", width=80)
        st.title("🔒 Acceso Privado: Barmel Corp")
        st.text_input("Introduce la contraseña empresarial:", type="password", on_change=password_entered, key="password")
        if "password_correct" in st.session_state:
            st.error("😕 Contraseña incorrecta.")
        return False
    return st.session_state["password_correct"]

# --- 2. EL COMPONENTE DE SEGURIDAD CONTROLA TODO ---
if check_password():
    # TODO LO QUE ESTÉ AQUÍ ADENTRO (CON ESTE ESPACIO A LA IZQUIERDA) SOLO SE VERÁ SI LA CLAVE ES CORRECTA
    st.success("✅ Acceso Autorizado - Michael Barahona")
    
    # Configuración de la App
    st.title("Barmel Corporation: Intelligent Translator")
    st.subheader("Herramienta Oficial de Traducción Técnica")
    st.markdown("---")

    # Tu lógica de traducción
    col1, col2 = st.columns(2)
    with col1:
        st.info("📂 Paso 1: Sube el manual o contrato en inglés")
        uploaded_file = st.file_uploader("", type=["pdf"])
        # ... aquí sigue el resto de tu código de traducción (asegúrate de que todo tenga sangría) ...
        if uploaded_file and st.button("🚀 INICIAR TRADUCCIÓN"):
             with st.spinner("Procesando para Barmel Corp..."):
                with pdfplumber.open(uploaded_file) as pdf:
                    texto_total = ""
                    for page in pdf.pages:
                        extract = page.extract_text()
                        if extract:
                            texto_total += GoogleTranslator(source='en', target='es').translate(extract) + "\n"
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