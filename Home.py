import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Trabalho Final Programação - Veículos Elétricos",
    page_icon="🚗",
    layout="wide"
)

# CSS simples apenas para fonte padrão (sem alterar títulos com HTML)
st.markdown(
    """
    <style>
    html, body, [class*="css"]  {
        font-family: Arial, Helvetica, sans-serif !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Títulos principais com Markdown
st.title("Trabalho Final de Programação")
st.subheader("Dupla: Gustavo Soares e Vítor Rodrigues")
st.markdown("## Análise de Veículos Elétricos no estado de Washington, EUA")
st.markdown("---")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('Electric_Vehicle_Population_Data.csv')
        return df
    except Exception as e:
        st.error(f"não deu {e}")
        return None

df = load_data()

if df is not None:
    st.metric("Número total de registros", f"{df.shape[0]:,}")
    st.markdown("---")

    st.markdown("## 🎯 Objetivo do Dashboard")
    st.markdown("""
O objetivo principal é facilitar a compreensão das características da frota de veículos elétricos,
identificando, por exemplo, os fabricantes mais populares, a evolução da adoção de EVs ao longo do tempo
e a distribuição geográfica.
""")

    st.markdown("---")
    st.markdown("## 📌 Como Navegar")
    st.markdown("""
Use a barra lateral à esquerda para acessar as diferentes seções:

### 📊 Visão Geral dos Dados
- Filtros por ano, tipo de veículo  
- Gráficos de barras, pizza e linha  
- Visão geral dos dados filtrados  

### 🏭 Análise Detalhada por Fabricantes
- Filtros específicos por fabricante  
- Evolução temporal por fabricante  
- Distribuição de tipos e modelos  
- Comparação entre fabricantes  
""")

    st.markdown("### Como os Filtros Influenciam")
    st.markdown("""
Em algumas páginas, você encontrará filtros na barra lateral.  
Esses filtros permitem que você refine os dados exibidos nos gráficos, possibilitando uma análise mais detalhada  
para um ano específico, tipo de veículo, ou outros critérios relevantes.  
Ao alterar os filtros, os gráficos serão automaticamente atualizados.
""")

    st.markdown("---")
    st.markdown("## 📈 Filtros limites")

    col1, col2 = st.columns(2)
    with col1:
        if 'Model Year' in df.columns:
            df['Model Year'] = pd.to_numeric(df['Model Year'], errors='coerce')
            ano_min = int(df['Model Year'].min())
            ano_max = int(df['Model Year'].max())
            st.write(f"**Período:** {ano_min} - {ano_max}")
        if 'Electric Vehicle Type' in df.columns:
            tipos = df['Electric Vehicle Type'].unique()
            st.write(f"**Tipos de Veículos:** {len(tipos)}")
    with col2:
        if 'City' in df.columns:
            cidades = df['City'].unique()
            st.write(f"**Cidades:** {len(cidades)}")
else:
    st.error("não deu")
