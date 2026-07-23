import streamlit as st

st.set_page_config(page_title="PIA & Risk Advisor", page_icon="🛡️", layout="wide")

if "respuestas_umbral" not in st.session_state:
    st.session_state.respuestas_umbral = {}

st.title("🛡️ PIA & Risk Advisor — Privacidad por Diseño")
st.caption("Herramienta interactiva para Evaluaciones de Impacto (EIPD) y Análisis de Riesgos")

# Criterios del Comité Europeo de Protección de Datos (CEPD)
criterios = {
    "evaluacion_perfilado": "1. Evaluación o puntuación (incluyendo el perfilado y la elaboración de perfiles).",
    "decisiones_automatizadas": "2. Toma de decisiones automatizadas con efectos jurídicos o significativos.",
    "observacion_sistematica": "3. Observación, supervisión o control sistemático de los interesados.",
    "datos_sensibles": "4. Tratamiento de datos sensibles o de carácter altamente personal (salud, biométricos, etc.).",
    "gran_escala": "5. Tratamiento de datos a gran escala.",
    "cruce_datos": "6. Asociación o combinación de conjuntos de datos de distintas fuentes.",
    "vulnerables": "7. Datos relativos a interesados vulnerables (menores, empleados, ancianos).",
    "tecnologias_nuevas": "8. Uso innovador o aplicación de nuevas soluciones tecnológicas.",
    "exclusion_derechos": "9. Tratamiento que impida a los interesados ejercer un derecho o utilizar un servicio."
}

st.header("📋 Módulo 1: ¿Es necesaria una EIPD?")
st.write("El RGPD exige una EIPD cuando el tratamiento implique un alto riesgo. Responde a los criterios clave:")

conteo_si = 0
st.markdown("---")

for clave, pregunta in criterios.items():
    valor_previo = st.session_state.respuestas_umbral.get(clave, "No")
    respuesta = st.radio(pregunta, ["No", "Sí"], index=0 if valor_previo == "No" else 1, horizontal=True, key=f"chk_{clave}")
    st.session_state.respuestas_umbral[clave] = respuesta
    if respuesta == "Sí":
        conteo_si += 1

st.markdown("---")
st.subheader("📊 Resultado del Análisis de Umbral")
st.metric(label="Criterios de alto riesgo detectados", value=f"{conteo_si} / 9")

if conteo_si >= 2:
    st.error("🚨 **EIPD OBLIGATORIA:** Se han detectado 2 o más criterios de alto riesgo. Debes realizar una Evaluación de Impacto completa.")
elif conteo_si == 1:
    st.warning("⚠️ **RECOMENDABLE:** Solo se cumple un criterio, pero se aconseja documentar un análisis de riesgos detallado.")
else:
    st.success("✅ **RIESGO INICIAL BAJO:** No se cumplen criterios automáticos de obligatoriedad.")
