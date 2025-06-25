import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("📊 Visão Geral dos Dados")

@st.cache_data
def load_data():
    df = pd.read_csv('Electric_Vehicle_Population_Data.csv')
    return df

df = load_data()


st.sidebar.header("🔧 Filtros")


if 'Model Year' in df.columns:
    df['Model Year'] = pd.to_numeric(df['Model Year'], errors='coerce')
    anos_disponiveis = sorted(df['Model Year'].dropna().unique())
    
    ano_min = st.sidebar.selectbox(
        "Ano Mínimo:",
        anos_disponiveis,
        index=0
    )
    
    ano_max = st.sidebar.selectbox(
        "Ano Máximo:",
        anos_disponiveis,
        index=len(anos_disponiveis)-1
    )
    
   
    df_filtrado = df[(df['Model Year'] >= ano_min) & (df['Model Year'] <= ano_max)]
else:
    df_filtrado = df


if 'Electric Vehicle Type' in df_filtrado.columns:
    tipos = ['Todos'] + sorted(df_filtrado['Electric Vehicle Type'].unique().tolist())
    tipo_selecionado = st.sidebar.selectbox(
        "Tipo de Veículo:",
        tipos
    )
    
    if tipo_selecionado != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['Electric Vehicle Type'] == tipo_selecionado]


st.sidebar.write("---")
st.sidebar.info(f"📊 **Dados filtrados:** {df_filtrado.shape[0]:,} registros")


st.subheader("🏭 Top 10 Fabricantes")
if 'Make' in df_filtrado.columns:
    top_fabricantes = df_filtrado['Make'].value_counts().head(10).reset_index()
    top_fabricantes.columns = ['Fabricante', 'Quantidade']
    
    fig1 = px.bar(
        top_fabricantes, 
        x='Fabricante', 
        y='Quantidade',
        title='Top 10 Fabricantes de Veículos Elétricos',
        color='Quantidade',
        color_continuous_scale='viridis'
    )
    fig1.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig1, use_container_width=True)

st.subheader("🔋 Distribuição por Tipo de Veículo")
if 'Electric Vehicle Type' in df_filtrado.columns:
    tipos_dist = df_filtrado['Electric Vehicle Type'].value_counts().reset_index()
    tipos_dist.columns = ['Tipo', 'Quantidade']
    
    fig2 = px.pie(
        tipos_dist,
        values='Quantidade',
        names='Tipo',
        title='Distribuição por Tipo de Veículo Elétrico',
        hole=0.3
    )
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("📈 Evolução ao Longo do Tempo")
if 'Model Year' in df_filtrado.columns:
    evolucao = df_filtrado['Model Year'].value_counts().sort_index().reset_index()
    evolucao.columns = ['Ano', 'Quantidade']
    
    fig3 = px.line(
        evolucao,
        x='Ano',
        y='Quantidade',
        title='Evolução dos Veículos Elétricos por Ano',
        markers=True
    )
    st.plotly_chart(fig3, use_container_width=True)


