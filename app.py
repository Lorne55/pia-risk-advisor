import streamlit as st
from catalogo import CATALOGO_AEPD

st.set_page_config(page_title="PIA & Risk Advisor", page_icon="🛡️", layout="wide")

if "respuestas_umbral" not in st.session_state: st.session_state.respuestas_umbral = {}
if "riesgos_evaluados" not in st.session_state: st.session_state.riesgos_evaluados = []
if "datos_empresa" not in st.session_state:
    st.session_state.datos_empresa = {"nombre": "", "nif": "", "dpd": "", "licitud": "Art. 6.1.a) Consentimiento del interesado"}

st.title("🛡️ PIA & Risk Advisor — Gestiona RGPD Premium")
st.caption("Herramienta interactiva alineada con la Guía de Gestión de Riesgos de la AEPD")

menu = st.sidebar.radio(
    "Módulos del Programa",
    ["1. Configuración y Umbral EIPD", "2. Registro de Riesgos (AEPD)", "3. Mitigación Inteligente", "4. Reporte e Informe Final"]
)

criterios_base = {
    "c1": "1. Evaluación o puntuación (incluyendo el perfilado).",
    "c2": "2. Toma de decisiones automatizadas con efectos jurídicos.",
    "c3": "3. Observación, supervisión o control sistemático.",
    "c4": "4. Tratamiento de datos sensibles (salud, biométricos, etc.).",
    "c5": "5. Tratamiento de datos a gran escala.",
    "c6": "6. Asociación o combinación de conjuntos de datos.",
    "c7": "7. Datos relativos a interesados vulnerables (menores, empleados).",
    "c8": "8. Uso innovador o aplicación de nuevas soluciones tecnológicas.",
    "c9": "9. Tratamiento que impida a los interesados ejercer un derecho."
}
conteo_si_global = sum(1 for k in criterios_base.keys() if st.session_state.respuestas_umbral.get(k, "No") == "Sí")
dictamen = "EIPD OBLIGATORIA (AEPD)" if conteo_si_global >= 2 else ("EIPD RECOMENDABLE" if conteo_si_global == 1 else "RIESGO ORDINARIO")

if menu == "1. Configuración y Umbral EIPD":
    st.header("🏢 1. Datos del Tratamiento (RAT) y Test de Umbral")
    col_e1, col_e2, col_e3 = st.columns(3)
    with col_e1: st.session_state.datos_empresa["nombre"] = st.text_input("Nombre de la Entidad / Responsable:", value=st.session_state.datos_empresa["nombre"])
    with col_e2: st.session_state.datos_empresa["nif"] = st.text_input("N.I.F. de la Entidad:", value=st.session_state.datos_empresa["nif"])
    with col_e3: st.session_state.datos_empresa["dpd"] = st.text_input("Delegado de Protección de Datos (DPD):", value=st.session_state.datos_empresa["dpd"])
    
    opciones_licitud = [
        "Art. 6.1.a) Consentimiento del interesado",
        "Art. 6.1.b) Ejecución de un contrato / medidas precontractuales",
        "Art. 6.1.c) Cumplimiento de una obligación legal",
        "Art. 6.1.d) Protección de intereses vitales",
        "Art. 6.1.e) Misión realizada en interés público / poderes públicos",
        "Art. 6.1.f) Satisfacción de intereses legítimos"
    ]
    st.session_state.datos_empresa["licitud"] = st.selectbox("Base de Licitud Jurídica del Tratamiento (Art. 6 RGPD):", opciones_licitud, index=opciones_licitud.index(st.session_state.datos_empresa["licitud"]) if st.session_state.datos_empresa["licitud"] in opciones_licitud else 0)
    
    st.markdown("---")
    st.subheader("📋 Análisis de Umbral CEPD / AEPD")
    conteo_si = 0
    for clave, pregunta in criterios_base.items():
        valor_previo = st.session_state.respuestas_umbral.get(clave, "No")
        respuesta = st.radio(pregunta, ["No", "Sí"], index=0 if valor_previo == "No" else 1, horizontal=True, key=f"chk_{clave}")
        st.session_state.respuestas_umbral[clave] = respuesta
        if respuesta == "Sí": conteo_si += 1
    
    st.markdown("---")
    st.metric(label="Criterios de alto riesgo detectados", value=f"{conteo_si} / 9")
    if conteo_si >= 2: st.error(f"🚨 **{dictamen}:** Se exigen metodologías avanzadas de control.")
    elif conteo_si == 1: st.warning(f"⚠️ **{dictamen}:** Justifique formalmente los controles elegidos.")
    else: st.success(f"✅ **{dictamen}:** Riesgo bajo bajo el marco general.")

elif menu == "2. Registro de Riesgos (AEPD)":
    st.header("🎲 2. Inventario de Factores de Riesgo / Amenazas")
    st.write("Conforme a la guía de la AEPD, asocie el tratamiento a un factor de riesgo técnico u organizativo.")
    with st.expander("➕ Identificar y clasificar nuevo factor de riesgo", expanded=True):
        operacion_sel = st.selectbox("Clasificación de la operación (según catálogo AEPD):", list(CATALOGO_AEPD.keys()))
        descripcion_riesgo = st.text_area("Escenario específico del riesgo detectado:", placeholder="Ej. Monitorización de tiempos de navegación sin política clara...")
        col1, col2 = st.columns(2)
        with col1: prob = st.slider("Probabilidad (1 = Muy Baja, 5 = Muy Alta):", 1, 5, 3, key="p_bruta")
        with col2: imp = st.slider("Impacto potencial (1 = Despreciable, 5 = Crítico):", 1, 5, 3, key="i_bruta")
        total_b = prob * imp
        nivel_b = "ALTO" if total_b >= 15 else "MEDIO" if total_b >= 8 else "BAJO"
        st.write(f"**Riesgo Inherente Bruto:** `{total_b} / 25` — Clasificación: **{nivel_b}**")
        if st.button("💾 Registrar Factor de Riesgo"):
            if not descripcion_riesgo.strip(): st.warning("Describa el escenario del riesgo.")
            else:
                st.session_state.riesgos_evaluados.append({
                    "operacion": operacion_sel, "descripcion": descripcion_riesgo, "probabilidad": prob, "impacto": imp,
                    "total": total_b, "nivel": nivel_b, "controles": [], "prob_residual": prob, "imp_residual": imp,
                    "total_residual": total_b, "nivel_residual": nivel_b
                })
                st.success("¡Factor de riesgo almacenado localmente!")
                st.rerun()
    st.markdown("---")
    st.subheader("📋 Factores de Riesgo Registrados en esta Sesión")
    if not st.session_state.riesgos_evaluados: st.info("Ningún riesgo registrado aún.")
    else:
        for idx, r in enumerate(st.session_state.riesgos_evaluados):
            col_icon = "🔴" if r["nivel"] == "ALTO" else "🟡" if r["nivel"] == "MEDIO" else "🟢"
            st.markdown(f"{col_icon} **#{idx+1} Operación: {r['operacion']}**")
            st.write(f"*Escenario:* {r['descripcion']}")
            st.write(f"**Métricas iniciales:** P: `{r['probabilidad']}` | I: `{r['impacto']}` | **Total Bruto: {r['total']} ({r['nivel']})**")
            st.markdown("---")
        if st.button("🗑️ Resetear matriz de riesgos"):
            st.session_state.riesgos_evaluados = []
            st.rerun()

elif menu == "3. Mitigación Inteligente":
    st.header("🛡️ 3. Aplicación de Medidas y Salvaguardas Oficiales AEPD")
    if not st.session_state.riesgos_evaluados: st.info("⚠️ Registre al menos un factor de riesgo en el Módulo 2 primero.")
    else:
        opciones = [f"#{i+1}: [{r['operacion']}] {r['descripcion'][:40]}..." for i, r in enumerate(st.session_state.riesgos_evaluados)]
        r_idx = st.selectbox("Seleccione el riesgo que desea mitigar:", range(len(opciones)), format_func=lambda x: opciones[x])
        r_act = st.session_state.riesgos_evaluados[r_idx]
        with st.form("form_mitigar"):
            medidas_sugeridas = CATALOGO_AEPD.get(r_act["operacion"], ["Otro control organizativo personalizado"])
            control_tipo = st.selectbox("Medida recomendada por la AEPD para esta operación:", medidas_sugeridas)
            control_detalles = st.text_input("Detalles específicos de implantación en la empresa:")
            st.markdown("**Reevaluación del Riesgo Residual (Post-Medida):**")
            col_m1, col_m2 = st.columns(2)
            with col_m1: n_p = st.slider("Nueva Probabilidad:", 1, 5, int(r_act["prob_residual"]))
            with col_m2: n_i = st.slider("Nuevo Impacto:", 1, 5, int(r_act["imp_residual"]))
            if st.form_submit_button("🛡️ Validar e Implantar Medida"):
                n_tot = n_p * n_i
                r_act["controles"].append(f"{control_tipo} -> Impl: {control_detalles}")
                r_act["prob_residual"], r_act["imp_residual"], r_act["total_residual"] = n_p, n_i, n_tot
                r_act["nivel_residual"] = "ALTO" if n_tot >= 15 else "MEDIO" if n_tot >= 8 else "BAJO"
                st.success("¡Medida asociada correctamente al factor de riesgo!")
                st.rerun()
        st.markdown("### 📊 Historial de Controles del Riesgo")
        if r_act["controles"]:
            for c in r_act["controles"]: st.write(f"- {c}")
            cm1, cm2 = st.columns(2)
            cm1.metric("Riesgo Bruto Inicial", f"{r_act['total']} / 25")
            cm2.metric("Riesgo Residual Final", f"{r_act['total_residual']} / 25", delta=f"{r_act['total_residual'] - r_act['total']}", delta_color="inverse")
        else: st.warning("Este factor de riesgo se encuentra actualmente sin mitigar.")

elif menu == "4. Reporte e Informe Final":
    st.header("📄 4. Acta de Cumplimiento Técnico y Gestión de Riesgos")
    emp = st.session_state.datos_empresa
    rep = "=== AUDITORÍA DE PRIVACIDAD: INFORME DE GESTIÓN DE RIESGOS ===\n\n"
    rep += "RESPONSABLE DEL TRATAMIENTO: " + str(emp['nombre'] if emp['nombre'] else 'No definido') + "\n"
    rep += "N.I.F. ENTIDAD: " + str(emp['nif'] if emp['nif'] else 'No definido') + "\n"
    rep += "DELEGADO DE PROTECCIÓN DE DATOS (DPD): " + str(emp['dpd'] if emp['dpd'] else 'No designado') + "\n"
    rep += "LICITUD JURÍDICA PRINCIPAL: " + str(emp['licitud']) + "\n\n"
    rep += "1. EVALUACIÓN DE UMBRAL (EXIGENCIA DE EIPD):\n"
    rep += "- Criterios CEPD/AEPD concurrentes: " + str(conteo_si_global) + " / 9\n"
    rep += "- Dictamen formal del sistema: " + str(dictamen) + "\n\n"
    rep += "2. TRATAMIENTOS ANALIZADOS Y MEDIDAS DE MITIGACIÓN APLICADAS:\n"
    if not st.session_state.riesgos_evaluados:
        rep += " No se han registrado análisis de riesgos específicos en esta sesión corporativa.\n"
    else:
        for idx, r in enumerate(st.session_state.riesgos_evaluados):
            rep += "\n[FACTOR #" + str(idx+1) + "] Operación de Riesgo: " + str(r['operacion']) + "\n"
            rep += " - Escenario de amenaza: " + str(r['descripcion']) + "\n"
            rep += " - Nivel Bruto Inicial: " + str(r['total']) + " (" + str(r['nivel']) + ")\n"
            rep += " - Controles Oficiales Aplicados (AEPD):\n"
            if r["controles"]:
                for c in r["controles"]: 
                    rep += "   * " + str(c) + "\n"
            else: 
                rep += "   * ALERTA: Sin medidas de mitigación aplicadas.\n"
            rep += " - Puntuación de Riesgo Residual Post-Control: " + str(r['total_residual']) + " (" + str(r['nivel_residual']) + ")\n"
            
    st.text_area("📋 Copiar Acta Oficial de Cumplimiento:", value=rep, height=450)
