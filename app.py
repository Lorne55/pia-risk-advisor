import streamlit as st

st.set_page_config(page_title="PIA & Risk Advisor", page_icon="🛡️", layout="wide")

if "respuestas_umbral" not in st.session_state:
    st.session_state.respuestas_umbral = {}
if "riesgos_evaluados" not in st.session_state:
    st.session_state.riesgos_evaluados = []

st.title("🛡️ PIA & Risk Advisor — Privacidad por Diseño")
st.caption("Herramienta interactiva para Evaluaciones de Impacto (EIPD) y Análisis de Riesgos")

# Sistema de pestañas ampliado a 3 módulos
tab1, tab2, tab3 = st.tabs(["📋 1. Test de Umbral (EIPD)", "🎲 2. Análisis de Riesgos", "🛡️ 3. Controles y Mitigación"])

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
            "Acceso indebido o no autorizado a los datos personales",
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
                    "nivel": nivel_texto,
                    "controles": [],
                    "prob_residual": probabilidad,
                    "imp_residual": impacto,
                    "total_residual": riesgo_total,
                    "nivel_residual": nivel_texto
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

# ==========================================
# PESTAÑA 3: CONTROLES Y RIESGO RESIDUAL
# ==========================================
with tab3:
    st.header("🛡️ Mitigación de Riesgos y Controles")
    st.write("Aplica medidas técnicas y organizativas a los riesgos que detectaste para mitigar su impacto o probabilidad.")

    if not st.session_state.riesgos_evaluados:
        st.info("⚠️ Primero debes registrar al menos un riesgo en la pestaña **2. Análisis de Riesgos** para poder mitigarlo aquí.")
    else:
        st.write("Selecciona un riesgo registrado para aplicarle medidas protectoras:")
        
        opciones_riesgos = [f"#{i+1}: {r['amenaza'][:50]}..." for i, r in enumerate(st.session_state.riesgos_evaluados)]
        riesgo_seleccionado_idx = st.selectbox("Elegir riesgo a mitigar:", range(len(opciones_riesgos)), format_func=lambda x: opciones_riesgos[x])
        
        r_actual = st.session_state.riesgos_evaluados[riesgo_seleccionado_idx]
        
        st.markdown(f"**Riesgo seleccionado:** *{r_actual['descripcion']}*")
        st.info(f"Riesgo Inicial: **{r_actual['total']} ({r_actual['nivel']})** [P: {r_actual['probabilidad']}, I: {r_actual['impacto']}]")
        
        with st.form("form_controles"):
            st.subheader("⚙️ Añadir Medida de Mitigación")
            controles_sugeridos = [
                "Cifrado de datos en reposo y en tránsito",
                "Autenticación de Doble Factor (2FA) para accesos",
                "Políticas estrictas de control de accesos (RBAC)",
                "Copias de seguridad periódicas y cifradas",
                "Formación y concienciación periódica al personal",
                "Acuerdo de Confidencialidad y NDA firmado",
                "Auditorías técnicas y test de penetración anuales",
                "Otro control específico"
            ]
            control_tipo = st.selectbox("Medida de seguridad / salvaguarda:", controles_sugeridos)
            control_detalles = st.text_input("Detalles de la implementación:", placeholder="Ej. Se implementará BitLocker en portátiles y cifrado AES-256.")
            
            st.markdown("**Reevalúa el riesgo tras aplicar este control (Riesgo Residual):**")
            col1, col2 = st.columns(2)
            with col1:
                nueva_p = st.slider("Nueva Probabilidad:", 1, 5, int(r_actual["prob_residual"]))
            with col2:
                nuevo_i = st.slider("Nuevo Impacto:", 1, 5, int(r_actual["imp_residual"]))
                
            if st.form_submit_button("🛡️ Aplicar y Actualizar Riesgo"):
                nuevo_total = nueva_p * nuevo_i
                nuevo_nivel = "ALTO" if nuevo_total >= 15 else "MEDIO" if nuevo_total >= 8 else "BAJO"
                
                r_actual["controles"].append(f"{control_tipo}: {control_detalles}")
                r_actual["prob_residual"] = nueva_p
                r_actual["imp_residual"] = nuevo_i
                r_actual["total_residual"] = nuevo_total
                r_actual["nivel_residual"] = nuevo_nivel
                
                st.success("¡Control aplicado con éxito!")
                st.rerun()

        st.markdown("### 📊 Estado de Mitigación Actual")
        if r_actual["controles"]:
            st.write("**Controles aplicados:**")
            for c in r_actual["controles"]:
                st.write(f"- {c}")
            
            c1, c2 = st.columns(2)
            c1.metric("Riesgo Bruto Inicial", f"{r_actual['total']} / 25", delta=None)
            c2.metric("Riesgo Residual Actual", f"{r_actual['total_residual']} / 25", delta=f"{r_actual['total_residual'] - r_actual['total']}", delta_color="inverse")
        else:
            st.warning("Este riesgo aún no cuenta con ningún control aplicado.")
            st.header("📄 Generación de Informe Técnico de Privacidad")
            st.write("A continuación se presenta el resumen consolidado de tu análisis. Puedes copiar este texto para guardar tu informe de auditoría.")
            st.markdown("---")

        dictamen = "EIPD OBLIGATORIA (2 o más criterios de alto riesgo)" if conteo_si_global >= 2 
    else: "EIPD RECOMENDABLE (1 criterio detectado)" if conteo_si_global == 1 
    else: "EIPD NO OBLIGATORIA (Riesgo Bajo)"
        reporte_texto = f"=== INFORME DE PRIVACIDAD POR DISEÑO Y RIESGOS ===\n\n"
        reporte_texto += f"1. TEST DE UMBRAL (EIPD):\n"
        reporte_texto += f"- Criterios de alto riesgo detectados: {conteo_si_global} / 9\n"
        reporte_texto += f"- Dictamen formal: {dictamen}\n\n"

reporte_texto += f"2. MATRIZ DE RIESGOS E IMPACTOS:\n"
if not st.session_state.riesgos_evaluados:
    reporte_texto += " No se han registrado riesgos en esta sesión.\n"
else:
    for idx, r in enumerate(st.session_state.riesgos_evaluados):
        reporte_texto += f"\n[Riesgo #{idx+1}] Amenaza: {r['amenaza']}\n"
        reporte_texto += f" - Descripción del escenario: {r['descripcion']}\n"
        reporte_texto += f" - Riesgo Inicial Bruto: {r['total']} ({r['nivel']}) [P:{r['probabilidad']}, I:{r['impacto']}]\n"
        reporte_texto += f" - Controles y Salvaguardas:\n"
        if r["controles"]:
            for c in r["controles"]:
                reporte_texto += f"   * {c}\n"
        else:
            reporte_texto += f"   * Ningún control registrado para esta amenaza.\n"
            reporte_texto += f" - Riesgo Residual Post-Control: {r['total_residual']} ({r['nivel_residual']}) [P:{r['prob_residual']}, I:{r['imp_residual']}]\n"
            st.text_area("📋 Resumen completo del informe:", value=reporte_texto, height=450)
            
            
        
        
