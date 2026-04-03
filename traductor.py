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
        
        voces = {
            "Español (México)": "com.mx",
            "Español (España)": "es",
            "Español (Estados Unidos)": "us"
        }
        voz_seleccionada = st.selectbox("Selecciona la voz de lectura:", options=list(voces.keys()))
        tld_seleccionado = voces[voz_seleccionada]

        if st.button("🔊 Escuchar (Generar Audio)"):
            with st.spinner("Generando audio..."):
                tts = gTTS(text=st.session_state.translated_text, lang='es', tld=tld_seleccionado)
                buf = io.BytesIO()
                tts.write_to_fp(buf)
                
                import base64
                import streamlit.components.v1 as components
                
                b64 = base64.b64encode(buf.getvalue()).decode()
                
                audio_html = f"""
                <div style="font-family: sans-serif; display: flex; flex-direction: column; align-items: center; background: #f9f9f9; padding: 15px; border-radius: 10px; border: 1px solid #ddd;">
                    <audio id="myAudio" controls style="width: 100%; margin-bottom: 15px; outline: none;">
                        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                    </audio>
                    <div style="display: flex; gap: 15px;">
                        <button id="rewindBtn" style="padding: 10px 20px; font-size: 16px; cursor: pointer; border-radius: 8px; border: 1px solid #ccc; background-color: #6c757d; color: white; font-weight: bold; transition: background 0.2s;">⏪ -5s</button>
                        <button id="forwardBtn" style="padding: 10px 20px; font-size: 16px; cursor: pointer; border-radius: 8px; border: 1px solid #ccc; background-color: #6c757d; color: white; font-weight: bold; transition: background 0.2s;">+5s ⏩</button>
                    </div>
                </div>
                <script>
                    const audio = document.getElementById('myAudio');
                    const rwBtn = document.getElementById('rewindBtn');
                    const fwBtn = document.getElementById('forwardBtn');

                    let holdInterval;
                    let isHolding = false;

                    const addHover = (btn) => {{
                        btn.onmouseover = () => btn.style.backgroundColor = '#5a6268';
                        btn.onmouseout = () => btn.style.backgroundColor = '#6c757d';
                    }};
                    addHover(rwBtn);
                    addHover(fwBtn);

                    const seek = (amount) => {{
                        if (!audio.duration) return;
                        let newTime = audio.currentTime + amount;
                        if (newTime < 0) newTime = 0;
                        if (newTime > audio.duration) newTime = audio.duration;
                        audio.currentTime = newTime;
                    }};

                    const startHold = (amount) => {{
                        if(isHolding) return;
                        isHolding = true;
                        seek(amount); // Salto inicial normal
                        
                        setTimeout(() => {{
                            if(isHolding) {{
                                holdInterval = setInterval(() => {{
                                    // Salta 0.3 segundos cada 100ms (Acelerado aprox x3)
                                    seek(amount > 0 ? 0.3 : -0.3);
                                }}, 100);
                            }}
                        }}, 400); 
                    }};

                    const stopHold = () => {{
                        isHolding = false;
                        clearInterval(holdInterval);
                    }};

                    rwBtn.addEventListener('mousedown', () => startHold(-5));
                    rwBtn.addEventListener('mouseup', stopHold);
                    rwBtn.addEventListener('mouseleave', stopHold);
                    rwBtn.addEventListener('touchstart', (e) => {{ e.preventDefault(); startHold(-5); }});
                    rwBtn.addEventListener('touchend', (e) => {{ e.preventDefault(); stopHold(); }});

                    fwBtn.addEventListener('mousedown', () => startHold(5));
                    fwBtn.addEventListener('mouseup', stopHold);
                    fwBtn.addEventListener('mouseleave', stopHold);
                    fwBtn.addEventListener('touchstart', (e) => {{ e.preventDefault(); startHold(5); }});
                    fwBtn.addEventListener('touchend', (e) => {{ e.preventDefault(); stopHold(); }});
                </script>
                """
                components.html(audio_html, height=180)

st.markdown("---")
st.caption("© 2026 Barmel Corporation | San Pedro Sula, Honduras. Uso exclusivo empresarial.")