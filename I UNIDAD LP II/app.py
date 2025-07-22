import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pyreadstat
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords
import openai
import io
import pymetaanalysis as pma
import networkx as nx
from matplotlib_venn import venn2
from fpdf import FPDF

# Inicializa NLTK stopwords
nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words('english'))

# Configura tu API Key de OpenAI (poner la tuya aquí)
openai.api_key = "TU_API_KEY_AQUI"

st.set_page_config(page_title="Análisis Completo Inteligente", layout="wide")

# -----------------
# Funciones auxiliares
# -----------------

def cargar_datos(file):
    if file is None:
        return None, None
    try:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
            tipo = 'datos'
        elif file.name.endswith('.xlsx'):
            df = pd.read_excel(file)
            tipo = 'datos'
        elif file.name.endswith('.txt'):
            df = pd.read_csv(file, delimiter='\t')
            tipo = 'datos'
        elif file.name.endswith('.sav'):
            df, meta = pyreadstat.read_sav(file)
            tipo = 'datos'
        elif file.name.endswith('.bib') or file.name.endswith('.ris'):
            texto = file.read().decode("utf-8")
            df = texto
            tipo = 'bibliometria'
        elif file.name.endswith('.json'):
            df = pd.read_json(file)
            tipo = 'datos'
        else:
            st.warning("Formato no soportado.")
            return None, None
        return df, tipo
    except Exception as e:
        st.error(f"Error cargando archivo: {e}")
        return None, None

def analisis_descriptivo(df):
    desc = df.describe(include='all').T
    return desc

def matriz_correlacion(df):
    return df.select_dtypes(include=np.number).corr()

def graficos_basicos(df):
    num_cols = df.select_dtypes(include=np.number).columns.tolist()
    figs = {}
    for col in num_cols:
        fig, ax = plt.subplots()
        sns.histplot(df[col].dropna(), kde=True, ax=ax)
        ax.set_title(f"Histograma de {col}")
        figs[f"hist_{col}"] = fig
        plt.close(fig)

        fig2, ax2 = plt.subplots()
        sns.boxplot(x=df[col], ax=ax2)
        ax2.set_title(f"Boxplot de {col}")
        figs[f"box_{col}"] = fig2
        plt.close(fig2)
    return figs

def prueba_t_anova(df):
    from scipy.stats import ttest_ind, f_oneway
    resultados = {}
    num_cols = df.select_dtypes(include=np.number).columns.tolist()
    cat_cols = df.select_dtypes(include=['category', 'object']).columns.tolist()
    for num in num_cols:
        for cat in cat_cols:
            groups = df.groupby(cat)[num]
            if groups.ngroups == 2:
                g1, g2 = [groups.get_group(g).dropna() for g in groups.groups]
                stat, p = ttest_ind(g1, g2)
                resultados[f"Prueba t de {num} por {cat}"] = (stat, p)
            elif groups.ngroups > 2:
                arrays = [groups.get_group(g).dropna() for g in groups.groups]
                stat, p = f_oneway(*arrays)
                resultados[f"ANOVA de {num} por {cat}"] = (stat, p)
    return resultados

def metaanalisis_completo(df):
    # Espera df con columnas 'effect_size', 'variance'
    try:
        model = pma.MetaAnalysis(df['effect_size'], df['variance'])
        res = model.fit()
        return model, res
    except Exception as e:
        st.error(f"Error metaanálisis: {e}")
        return None, None

def analisis_bibliometria(texto):
    palabras = nltk.word_tokenize(texto.lower())
    palabras = [w for w in palabras if w.isalpha() and w not in stop_words]
    freq = pd.Series(palabras).value_counts()
    return freq

def generar_nube_palabras(freq):
    wc = WordCloud(width=800, height=400, background_color='white')
    wordcloud = wc.generate_from_frequencies(freq.to_dict())
    fig, ax = plt.subplots(figsize=(10,5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    return fig

def red_coocurrencia(texto, ventana=3):
    palabras = nltk.word_tokenize(texto.lower())
    palabras = [w for w in palabras if w.isalpha() and w not in stop_words]
    G = nx.Graph()
    for i, palabra in enumerate(palabras):
        for j in range(i+1, min(i+ventana+1, len(palabras))):
            w2 = palabras[j]
            if G.has_edge(palabra, w2):
                G[palabra][w2]['weight'] += 1
            else:
                G.add_edge(palabra, w2, weight=1)
    return G

def graficar_red(G, top_n=30):
    plt.figure(figsize=(12,12))
    weights = [G[u][v]['weight'] for u,v in G.edges()]
    nodes = sorted(G.degree, key=lambda x: x[1], reverse=True)[:top_n]
    nodes_set = set(n[0] for n in nodes)
    H = G.subgraph(nodes_set)
    pos = nx.spring_layout(H, k=0.5)
    nx.draw_networkx_nodes(H, pos, node_size=500, node_color='lightblue')
    nx.draw_networkx_edges(H, pos, width=[H[u][v]['weight'] for u,v in H.edges()])
    nx.draw_networkx_labels(H, pos, font_size=10)
    plt.title("Red de Co-ocurrencias (top palabras)")
    plt.axis('off')
    st.pyplot(plt.gcf())
    plt.close()

def interpretacion_ia(texto):
    prompt = f"Eres un experto estadístico y bibliométrico. Analiza y comenta este resumen:\n\n{texto}\n\nHaz recomendaciones claras y concisas."
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content":prompt}],
            max_tokens=400,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error en IA: {e}"

def generar_reporte_pdf(analisis_texto, graficos):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, analisis_texto)
    # No incluye gráficos en esta versión básica, se puede extender
    return pdf.output(dest='S').encode('latin-1')

# -----------------
# INTERFAZ STREAMLIT
# -----------------

st.title("🔍 Análisis Completo con IA, Bibliometría y Metaanálisis")

tab1, tab2, tab3, tab4 = st.tabs(["Carga y Datos", "Análisis Estadístico", "Bibliometría", "Metaanálisis"])

with tab1:
    st.header("📂 Carga de archivos")
    archivo = st.file_uploader("Sube datos o archivo bibliográfico", type=["csv","xlsx","txt","sav","bib","ris","json"])

    if archivo:
        df, tipo = cargar_datos(archivo)
        if df is not None:
            st.success(f"Archivo cargado tipo: {tipo}")
            if tipo == 'datos':
                st.dataframe(df.head())
            else:
                st.text(df[:500])

with tab2:
    st.header("📊 Análisis Estadístico")
    if 'df' in locals() and tipo == 'datos':
        st.subheader("Descriptivas")
        desc = analisis_descriptivo(df)
        st.dataframe(desc)

        st.subheader("Matriz de Correlación")
        corr = matriz_correlacion(df)
        st.dataframe(corr)

        st.subheader("Gráficos básicos")
        figs = graficos_basicos(df)
        for key, fig in figs.items():
            st.pyplot(fig)

        st.subheader("Pruebas estadísticas")
        resultados_pruebas = prueba_t_anova(df)
        for k,v in resultados_pruebas.items():
            stat, p = v
            st.write(f"{k}: Estadístico={stat:.3f}, p-valor={p:.4f}")

        st.subheader("Interpretación IA estadística")
        if st.button("Generar interpretación IA estadística"):
            resumen_str = desc.to_string()
            ia_res = interpretacion_ia(resumen_str)
            st.markdown(ia_res)
    else:
        st.info("Carga un archivo tipo datos para análisis estadístico.")

with tab3:
    st.header("📚 Bibliometría")
    if 'df' in locals() and tipo == 'bibliometria':
        freq = analisis_bibliometria(df)
        st.write("Frecuencia palabras top 20")
        st.dataframe(freq.head(20))

        st.subheader("Nube de palabras")
        fig_wc = generar_nube_palabras(freq)
        st.pyplot(fig_wc)

        st.subheader("Red de co-ocurrencias")
        G = red_coocurrencia(df)
        graficar_red(G)

        st.subheader("Interpretación IA bibliométrica")
        if st.button("Generar interpretación IA bibliométrica"):
            ia_res = interpretacion_ia(df[:2000])  # limitar tamaño
            st.markdown(ia_res)
    else:
        st.info("Carga un archivo bibliográfico (.bib, .ris) para bibliometría.")

with tab4:
    st.header("📈 Metaanálisis")
    meta_file = st.file_uploader("Archivo CSV con columnas 'effect_size' y 'variance'", type=["csv"], key="meta")
    if meta_file is not None:
        meta_df = pd.read_csv(meta_file)
        if {'effect_size', 'variance'}.issubset(meta_df.columns):
            model, res = metaanalisis_completo(meta_df)
            if res:
                st.write(res.summary())
                fig, ax = plt.subplots(figsize=(7,5))
                model.forest_plot(ax=ax)
                st.pyplot(fig)

                fig2, ax2 = plt.subplots(figsize=(6,6))
                model.funnel_plot(ax=ax2)
                st.pyplot(fig2)

                st.subheader("Interpretación IA metaanálisis")
                if st.button("Generar interpretación IA metaanálisis"):
                    ia_res = interpretacion_ia(str(res.summary()))
                    st.markdown(ia_res)
        else:
            st.error("El archivo debe contener las columnas 'effect_size' y 'variance'.")

# -----------------------------------------
# Botón para generar reporte completo PDF
# -----------------------------------------
if st.button("📄 Generar reporte PDF completo"):
    texto_reporte = "Reporte generado automáticamente.\n\n"
    if 'desc' in locals():
        texto_reporte += "Estadísticas Descriptivas:\n" + desc.to_string() + "\n\n"
    if 'corr' in locals():
        texto_reporte += "Matriz de Correlación:\n" + corr.to_string() + "\n\n"
    if 'resultados_pruebas' in locals():
        texto_reporte += "Resultados Pruebas:\n"
        for k,v in resultados_pruebas.items():
            texto_reporte += f"{k}: Estadístico={v[0]:.3f}, p-valor={v[1]:.4f}\n"
    pdf_bytes = generar_reporte_pdf(texto_reporte, None)
    st.download_button("Descargar Reporte PDF", pdf_bytes, file_name="reporte_analisis.pdf", mime="application/pdf")
