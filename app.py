import streamlit as st

# Configuración de la página
st.set_page_config(page_title="PIA & Risk Advisor", page_icon="🛡️", layout="wide")

# Inicializar estados de la sesión (Base de datos temporal en memoria)
if "respuestas_umbral" not in st.session_state:
    st.session_state.respuestas_umbral = {}

# Título Principal
st.title("🛡️ PIA & Risk Advisor — Privacidad por Diseño")
st.caption("Herramienta interactiva para Evaluaciones de Impacto (EIPD) y Análisis de Riesgos")

# Navegación Lateral (Estructura completa del proyecto)
menu = st.sidebar.radio(
    "Módulos del Programa",
    ["1. Test de Umbral (EIPD)", "2. Análisis de Riesgos", "3. Controles y Riesgo Residual", "4. Reporte Final"]
)

# ==========================================
# MÓDULO 1: TEST DE UMBRAL (EIPD)
# ==========================================
if menu == "1. Test de Umbral (EIPD)":
    st.header("📋 Evaluación Preliminar: ¿Es necesaria una EIPD?")
    st.write("El RGPD exige una EIPD cuando el tratamiento implique un alto riesgo para los derechos de las personas. Responde a los criterios clave:")

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

    # Formulario dinámico
    conteo_si = 0
    st.markdown("---")
    
    for clave, pregunta in criterios.items():
        # Guardar estado en session_state para no perderlo al cambiar de pestaña
        valor_previo = st.session_state.respuestas_umbral.get(clave, "No")
        respuesta = st.radio(pregunta, ["No", "Sí"], index=0 if valor_previo == "No" else 1, horizontal=True, key=f"chk_{clave}")
        st.session_state.respuestas_umbral[clave] = respuesta
        if respuesta == "Sí":
            conteo_si += 1

    # Lógica de Evaluación (Regla general: 2 o más criterios = EIPD obligatoria)
    st.markdown("---")
    st.subheader("📊 Resultado del Análisis de Umbral")
    st.metric(label="Criterios de alto riesgo detectados", value=f"{conteo_si} / 9")

    if conteo_si >= 2:
        st.error("🚨 **EIPD OBLIGATORIA:** Se han detectado 2 o más criterios de alto riesgo. Debes realizar una Evaluación de Impacto completa.")
    elif conteo_si == 1:
        st.warning("⚠️ **RECOMENDABLE:** Solo se cumple un criterio, pero se aconseja documentar un análisis de riesgos detallado para justificar si se realiza o no la EIPD.")
    else:
        st.success("✅ **RIESGO INICIAL BAJO:** No se cumplen criterios automáticos de obligatoriedad. Puedes continuar con un análisis de riesgos ordinario.")

# ==========================================
# MÓDULOS EN DESARROLLO (Marcadores de posición)
# ==========================================
elif menu == "2. Análisis de Riesgos":
    st.header("🎲 Matriz e Identificación de Riesgos")
    st.info("Aquí desarrollaremos el inventario de amenazas (accesos no autorizados, fugas, etc.) y la evaluación de Probabilidad x Impacto.")
    st.write("Próximamente: Controles interactivos para mapear amenazas.")

elif menu == "3. Controles y Riesgo Residual":
    st.header("🛡️ Mitigación de Riesgos y Controles")
    st.info("Aquí listaremos los controles (cifrado, copias de seguridad, formación) y calcularemos cómo reducen el riesgo inicial.")

elif menu == "4. Reporte Final":
    st.header("📄 Generación de Informe")
    st.info("Módulo para exportar todos los datos introducidos en un documento limpio o PDF listo para auditoría.")
