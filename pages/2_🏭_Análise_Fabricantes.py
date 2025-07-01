import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("🏭 Análise Detalhada por Fabricantes")

@st.cache_data
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

st.sidebar.write("---")
st.sidebar.info(f"📊 **Registros:** {df_filtrado.shape[0]:,}")

# Gráfico 1: Evolução dos 3 principais modelos do fabricante ao longo dos anos (barras agrupadas)
st.subheader("📈 Evolução dos 3 Principais Modelos ao Longo do Tempo")
if 'Model Year' in df_filtrado.columns and 'Model' in df_filtrado.columns and not df_filtrado.empty:
    top3_modelos = df_filtrado['Model'].value_counts().head(3).index.tolist()
    df_top3 = df_filtrado[df_filtrado['Model'].isin(top3_modelos)]
    evolucao_modelos = df_top3.groupby(['Model Year', 'Model']).size().reset_index(name='Quantidade')
    fig1 = px.bar(
        evolucao_modelos,
        x='Model Year',
        y='Quantidade',
        color='Model',
        barmode='group',
        title=f'Evolução dos 3 Principais Modelos de {fabricante_selecionado}'
    )
    st.plotly_chart(fig1, use_container_width=True)

# Gráfico 2: Tipos de veículos por fabricante (barras horizontais)
st.subheader("🔋 Tipos de Veículos por Fabricante")
if 'Electric Vehicle Type' in df_filtrado.columns and not df_filtrado.empty:
    tipos_fabricante = df_filtrado['Electric Vehicle Type'].value_counts().reset_index()
    tipos_fabricante.columns = ['Tipo', 'Quantidade']
    fig2 = px.bar(
        tipos_fabricante,
        x='Quantidade',
        y='Tipo',
        orientation='h',
        title=f'Distribuição de Tipos de Veículos - {fabricante_selecionado}',
        color='Tipo'
    )
    st.plotly_chart(fig2, use_container_width=True)



# Gráfico 4: Comparação entre fabricantes (dispersão)
if fabricante_selecionado == 'Todos':
    st.subheader("🏆 Comparação entre Fabricantes (Dispersão)")
    if 'Make' in df_filtrado.columns and 'Model Year' in df_filtrado.columns:
        fabricantes = df_filtrado.groupby('Make').agg(
            Quantidade=('Make', 'count'),
            AnoMedio=('Model Year', 'mean')
        ).reset_index()
        top_15 = fabricantes.nlargest(15, 'Quantidade')
        fig4 = px.scatter(
            top_15,
            x='AnoMedio',
            y='Quantidade',
            text='Make',
            size='Quantidade',
            color='Quantidade',
            title='Top 15 Fabricantes: Quantidade x Ano Médio'
        )
        fig4.update_traces(textposition='top center')
        st.plotly_chart(fig4, use_container_width=True)