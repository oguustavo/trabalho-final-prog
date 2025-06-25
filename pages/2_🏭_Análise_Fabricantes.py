import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(layout="wide")

st.title("🏭 Análise Detalhada por Fabricantes")


def load_data():
    df = pd.read_csv('Electric_Vehicle_Population_Data.csv')
    return df

df = load_data()


st.sidebar.header("🔧 Filtros para Fabricantes")

if 'Make' in df.columns:
    fabricantes = ['Todos'] + sorted(df['Make'].unique().tolist())
    fabricante_selecionado = st.sidebar.selectbox(
        "Selecione um Fabricante:",
        fabricantes
    )
    
    if fabricante_selecionado != 'Todos':
        df_filtrado = df[df['Make'] == fabricante_selecionado]
    else:
        df_filtrado = df
else:
    df_filtrado = df

if 'Model Year' in df_filtrado.columns:
    df_filtrado['Model Year'] = pd.to_numeric(df_filtrado['Model Year'], errors='coerce')
    anos_fabricante = sorted(df_filtrado['Model Year'].dropna().unique())
    
    if len(anos_fabricante) > 0:
        ano_inicio = st.sidebar.selectbox(
            "Ano de Início:",
            anos_fabricante,
            index=0
        )
        
        ano_fim = st.sidebar.selectbox(
            "Ano de Fim:",
            anos_fabricante,
            index=len(anos_fabricante)-1
        )
        
        df_filtrado = df_filtrado[
            (df_filtrado['Model Year'] >= ano_inicio) & 
            (df_filtrado['Model Year'] <= ano_fim)
        ]


st.sidebar.write("---")
st.sidebar.info(f"📊 **Registros:** {df_filtrado.shape[0]:,}")




st.subheader("📈 Evolução do Fabricante ao Longo do Tempo")
if 'Model Year' in df_filtrado.columns and not df_filtrado.empty:
    evolucao_fabricante = df_filtrado['Model Year'].value_counts().sort_index().reset_index()
    evolucao_fabricante.columns = ['Ano', 'Quantidade']
    
    fig1 = px.line(
        evolucao_fabricante,
        x='Ano',
        y='Quantidade',
        title=f'Evolução de {fabricante_selecionado} ao Longo dos Anos',
        markers=True,
        line_shape='linear'
    )
    fig1.update_layout(
        xaxis_title="Ano do Modelo",
        yaxis_title="Número de Veículos"
    )
    st.plotly_chart(fig1, use_container_width=True)


st.subheader("🔋 Tipos de Veículos por Fabricante")
if 'Electric Vehicle Type' in df_filtrado.columns and not df_filtrado.empty:
    tipos_fabricante = df_filtrado['Electric Vehicle Type'].value_counts().reset_index()
    tipos_fabricante.columns = ['Tipo', 'Quantidade']
    
    fig2 = px.pie(
        tipos_fabricante,
        values='Quantidade',
        names='Tipo',
        title=f'Distribuição de Tipos de Veículos - {fabricante_selecionado}',
        hole=0.4
    )
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("🚗 Top 10 Modelos do Fabricante")
if 'Model' in df_filtrado.columns and not df_filtrado.empty:
    modelos_fabricante = df_filtrado['Model'].value_counts().head(10).reset_index()
    modelos_fabricante.columns = ['Modelo', 'Quantidade']
    
    fig3 = px.bar(
        modelos_fabricante,
        x='Modelo',
        y='Quantidade',
        title=f'Top 10 Modelos - {fabricante_selecionado}',
        color='Quantidade',
        color_continuous_scale='plasma'
    )
    fig3.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig3, use_container_width=True)


if fabricante_selecionado == 'Todos':
    st.subheader("🏆 Comparação entre Fabricantes")
    
    
    top_15_fabricantes = df_filtrado['Make'].value_counts().head(15).reset_index()
    top_15_fabricantes.columns = ['Fabricante', 'Quantidade']
    
    fig4 = px.bar(
        top_15_fabricantes,
        x='Fabricante',
        y='Quantidade',
        title='Top 15 Fabricantes de Veículos Elétricos',
        color='Quantidade',
        color_continuous_scale='viridis'
    )
    fig4.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig4, use_container_width=True)




