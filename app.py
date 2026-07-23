import streamlit as st

st.set_page_config(page_title="PIA & Risk Advisor", page_icon="🛡️", layout="wide")

if "respuestas_umbral" not in st.session_state:
    st.session_state.respuestas_umbral = {}
if "riesgos_evaluados" not in st.session_state:
    st.session_state.riesgos_evaluados = []

st.title("🛡️ PIA & Risk Advisor — Privacidad por Diseño")
st.caption("Herramienta interactiva para Evaluaciones de Impacto (EIPD) y Análisis de Riesgos")

# Sistema de pestañas para navegar sin errores de sintaxis
tab1, tab2 = st.tabs(["📋 1. Test de Umbral (EIPD)", "🎲 2. Análisis de Riesgos"])

# ==========================================
# PESTAÑA 1: TEST DE UMBRAL (EIPD)
# ==========================================
with tab1:
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

    st.header("📋 Evaluación Preliminar: ¿Es necesaria una EIPD?")
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

# ==========================================
# PESTAÑA 2: ANÁLISIS DE RIESGOS INHERENTES
# ==========================================
with tab2:
    st.header("🎲 Identificación y Matriz de Riesgos")
    st.write("Identifica las amenazas potenciales sobre los datos y evalúa su riesgo bruto (sin controles aplicados).")

    with st.expander("➕ Evaluar una nueva amenaza / escenario de riesgo", expanded=True):
        amenazas_comunes = [
            "Acceso indebido o no unauthorized a los datos personales",
            "Alteración o manipulación fraudulenta de la información",
            "Pérdida accidental o destrucción física/lógica de bases de datos",
            "Fuga de información confidencial por Phishing / Malware",
            "Uso de los datos para finalidades distintas a las informadas",
            "Conservación de los datos más tiempo del límite legal",
            "Otro escenario personalizado"
        ]
        
        amenaza_sel = st.selectbox("Selecciona una amenaza tipo:", amenazas_comunes)
        descripcion_riesgo = st.text_area("Descripción específica del escenario:", placeholder="Ej. Acceso a la base de datos de clientes desde redes domésticas sin VPN...", key="txt_desc")
        
        col1, col2 = st.columns(2)
        with col1:
            probabilidad = st.slider("Probabilidad (1 = Muy Baja, 5 = Muy Alta):", 1, 5, 3, key="prob_inh")
        with col2:
            impacto = st.slider("Impacto en derechos (1 = Despreciable, 5 = Crítico):", 1, 5, 3, key="imp_inh")
        
        riesgo_total = probabilidad * impacto
        nivel_texto = "ALTO" if riesgo_total >= 15 else "MEDIO" if riesgo_total >= 8 else "BAJO"
            
        st.markdown(f"**Puntuación de Riesgo Inherente:** `{riesgo_total} / 25` — Nivel: **{nivel_texto}**")
        
        if st.button("💾 Guardar y Registrar Riesgo"):
            if descripcion_riesgo.strip() == "":
                st.warning("Por favor, describe el escenario específico antes de guardar.")
            else:
                nuevo_riesgo = {
                    "amenaza": amenaza_sel,
                    "descripcion": descripcion_riesgo,
                    "probabilidad": probabilidad,
                    "impacto": impacto,
                    "total": riesgo_total,
                    "nivel": nivel_texto
                }
                st.session_state.riesgos_evaluados.append(nuevo_riesgo)
                st.success("¡Riesgo guardado con éxito! Revisa el inventario abajo.")

    st.markdown("---")
    st.subheader("📋 Inventario de Riesgos Registrados")
    
    if not st.session_state.riesgos_evaluados:
        st.info("Aún no has registrado riesgos. Usa el formulario de arriba para añadir el primero.")
    else:
        for idx, r in enumerate(st.session_state.riesgos_evaluados):
            color = "🔴" if r["nivel"] == "ALTO" else "🟡" if r["nivel"] == "MEDIO" else "🟢"
            st.markdown(f"{color} **Riesgo #{idx+1}: {r['amenaza']}**")
            st.write(f"*Escenario:* {r['descripcion']}")
            st.write(f"**Métricas Iniciales:** Probabilidad: `{r['probabilidad']}` | Impacto: `{r['impacto']}` | **Total Bruto: {r['total']} ({r['nivel']})**")
            st.markdown("---")
                
        if st.button("🗑️ Borrar todos los riesgos"):
            st.session_state.riesgos_evaluados = []
            st.rerun()
