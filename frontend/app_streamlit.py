# frontend/app_streamlit.py
import streamlit as st
import requests

st.title("Prototipo de Gobernanza de Sistemas de Información de la UE")
st.write("Sube un documento PDF y analiza los posibles impactos en los componentes del sistema.")

uploaded_file = st.file_uploader("Sube un PDF", type=["pdf"])

if uploaded_file is not None:
    st.info("Procesando documento...")
    
    response = requests.post(
        "http://127.0.0.1:8000/analyze",
        files={"file": uploaded_file.getvalue()}
    )
    
    if response.status_code == 200:
        data = response.json()
        results = data.get("results", [])

        if not results:
            st.warning("No se detectaron impactos en los componentes.")
        else:
            st.success(f"Se detectaron {len(results)} componentes afectados:")

            for i, comp in enumerate(results):
                
                # 🔹 CORRECTO: usar claves del backend
                nombre = comp.get("component_name", "Desconocido")
                tipo = comp.get("tipo", "Desconocido")
                score = comp.get("final_score")

                # Score seguro
                score_text = "N/A" if score is None else f"{score:.2f}"

                # Impacto
                impact = comp.get("impact", "N/A")

                st.subheader(f"{nombre} ({tipo})")
                st.write(f"Impacto: **{impact}**")
                st.write(f"Puntuación: {score_text}")

                # 🔹 Mostrar desglose
                scores = comp.get("scores", {})
                st.caption(
                    f"Keyword: {scores.get('keyword',0):.2f} | "
                    f"Semantic: {scores.get('semantic',0):.2f} | "
                    f"Entity: {scores.get('entity',0):.2f}"
                )

                # 🔹 Fragmentos correctos
                fragments = comp.get("top_fragments", [])

                if fragments:
                    st.markdown("**Fragmentos relevantes:**")
                    for j, fr in enumerate(fragments):
                        st.text_area(
                            f"Fragmento {j+1}",
                            fr.get("fragment", ""),
                            height=120,
                            key=f"{i}_fragment_{j}"
                        )
                else:
                    st.write("No se encontraron fragmentos relevantes.")
    else:
        st.error(f"Error en el análisis: {response.status_code} - {response.text}")