import streamlit as st

st.set_page_config(page_title="PIA & Risk Advisor", page_icon="🛡️", layout="wide")

if "respuestas_umbral" not in st.session_state:
    st.session_state.respuestas_umbral = {}
if "riesgos_evaluados" not in st.session_state:
    st.session_state.riesgos_evaluados = []

st.title("🛡️ PIA & Risk Advisor")
st.caption("Herramienta interactiva para EIPD y Análisis de Riesgos")

menu = st.sidebar.radio(
    "Módulos del Programa",
    ["1. Test de Umbral (EIPD)", "2. Análisis de Riesgos Inherentes", "3. Controles y Riesgo Residual", "4. Reporte e Informe Final"]
)

criterios_base = {
    "c1": "1. Evaluación o puntuación (perfilado).",
    "c2": "2. Toma de decisiones automatizadas con efectos jurídicos.",
    "c3": "3. Observación, supervisión o control sistemático.",
    "c4": "4. Tratamiento de datos sensibles o altamente personales.",
    "c5": "5. Tratamiento de datos a gran escala.",
    "c6": "6. Asociación o combinación de conjuntos de datos.",
    "c7": "7. Datos relativos a interesados vulnerables.",
    "c8": "8. Uso innovador o aplicación de nuevas tecnologías.",
    "c9": "9. Tratamiento que impida ejercer un derecho."
}

conteo_si_global = sum(1 for k in criterios_base.keys() if st.session_state.respuestas_umbral.get(k, "No") == "Sí")
dictamen = "EIPD OBLIGATORIA" if conteo_si_global >= 2 else ("EIPD RECOMENDABLE" if conteo_si_global == 1 else "RIESGO BAJO")

if menu == "1. Test de Umbral (EIPD)":
    st.header("📋 Módulo 1: ¿Es necesaria una EIPD?")
    conteo_si = 0
    for clave, pregunta in criterios_base.items():
        valor_previo = st.session_state.respuestas_umbral.get(clave, "No")
        respuesta = st.radio(pregunta, ["No", "Sí"], index=0 if valor_previo == "No" else 1, horizontal=True, key=f"chk_{clave}")
        st.session_state.respuestas_umbral[clave] = respuesta
        if respuesta == "Sí":
            conteo_si += 1
    st.metric(label="Criterios detectados", value=f"{conteo_si} / 9")
    if conteo_si >= 2:
        st.error("🚨 EIPD OBLIGATORIA: Realiza una Evaluación de Impacto completa.")
    elif conteo_si == 1:
        st.warning("⚠️ RECOMENDABLE: Se aconseja documentar un análisis de riesgos.")
    else:
        st.success("✅ RIESGO INICIAL BAJO: Continúa con un análisis ordinario.")

elif menu == "2. Análisis de Riesgos Inherentes":
    st.header("🎲 Módulo 2: Matriz de Riesgos")
    with st.expander("➕ Evaluar una nueva amenaza", expanded=True):
        amenazas_comunes = ["Acceso indebido", "Alteración fraudulenta", "Pérdida accidental", "Fuga por Phishing", "Finalidad distinta", "Conservación excesiva", "Otro escenario"]
        amenaza_sel = st.selectbox("Selecciona una amenaza tipo:", amenazas_comunes)
        descripcion_riesgo = st.text_area("Descripción específica:", placeholder="Ej. Acceso sin VPN...", key="txt_desc")
        col1, col2 = st.columns(2)
        with col1:
            probabilidad = st.slider("Probabilidad (1-5):", 1, 5, 3, key="prob_inh")
        with col2:
            impacto = st.slider("Impacto (1-5):", 1, 5, 3, key="imp_inh")
        riesgo_total = probabilidad * impacto
        nivel_texto = "ALTO" if riesgo_total >= 15 else "MEDIO" if riesgo_total >= 8 else "BAJO"
        st.write(f"Riesgo: {riesgo_total} - Nivel: {nivel_texto}")
        if st.button("💾 Guardar Riesgo"):
            if descripcion_riesgo.strip() == "":
                st.warning("Escribe una descripción.")
            else:
                st.session_state.riesgos_evaluados.append({
                    "amenaza": threat_sel, "descripcion": descripcion_riesgo, "probabilidad": probabilidad, "impacto": impacto,
                    "total": riesgo_total, "nivel": nivel_texto, "controles": [], "prob_residual": probabilidad,
                    "imp_residual": impacto, "total_residual": riesgo_total, "nivel_residual": nivel_texto
                })
                st.success("¡Riesgo guardado!")
    if st.session_state.riesgos_evaluados:
        for idx, r in enumerate(st.session_state.riesgos_evaluados):
            st.write(f"#{idx+1}: {r['amenaza']} ({r['nivel']})")
        if st.button("🗑️ Borrar todos"):
            st.session_state.riesgos_evaluados = []
            st.rerun()

elif menu == "3. Controles y Riesgo Residual":
    st.header("🛡️ Módulo 3: Mitigación")
    if not st.session_state.riesgos_evaluados:
        st.info("⚠️ Registra un riesgo en el módulo 2 primero.")
    else:
        opciones_riesgos = [f"#{i+1}: {r['amenaza']}" for i, r in enumerate(st.session_state.riesgos_evaluados)]
        riesgo_seleccionado_idx = st.selectbox("Elegir riesgo:", range(len(opciones_riesgos)), format_func=lambda x: opciones_riesgos[x])
        r_actual = st.session_state.riesgos_evaluados[riesgo_seleccionado_idx]
        with st.form("form_controles"):
            control_tipo = st.selectbox("Salvaguarda:", ["Cifrado", "2FA", "Control de accesos", "Copias de seguridad", "Formación", "NDA", "Auditorías"])
            control_detalles = st.text_input("Detalles:")
            col1, col2 = st.columns(2)
            with col1:
                nueva_p = st.slider("Nueva Probabilidad:", 1, 5, int(r_actual["prob_residual"]))
            with col2:
                nuevo_i = st.slider("Nuevo Impacto:", 1, 5, int(r_actual["imp_residual"]))
            if st.form_submit_button("🛡️ Aplicar"):
                nuevo_total = nueva_p * nuevo_i
                r_actual["controles"].append(f"{control_tipo}: {control_detalles}")
                r_actual["prob_residual"], r_actual["imp_residual"], r_actual["total_residual"] = nueva_p, nuevo_i, nuevo_total
                r_actual["nivel_residual"] = "ALTO" if nuevo_total >= 15 else "MEDIO" if nuevo_total >= 8 else "BAJO"
                st.success("¡Aplicado!")
                st.rerun()

elif menu == "4. Reporte e Informe Final":
    st.header("📄 Módulo 4: Informe Final")
    reporte_texto = "=== INFORME DE PRIVACIDAD ===\n\n1. TEST DE UMBRAL:\n- Criterios: " + str(conteo_si_global) + "\n- Dictamen: " + str(dictamen) + "\n\n2. RIESGOS:\n"
    for idx, r in enumerate(st.session_state.riesgos_evaluados):
        reporte_texto += f"\n[Riesgo #{idx+1}] {r['amenaza']}\n - Inicial: {r['total']} ({r['nivel']})\n - Residual: {r['total_residual']} ({r['nivel_residual']})\n"
    st.text_area("Reporte:", value=reporte_texto, height=300)
