import pandas as pd
import streamlit as st
import altair as alt
import plotly.express as px

@st.cache
def busca_dados():
    # importando os dados
    df = pd.read_excel('controle.xlsx', index_col=0)
    df['Status'] = df.PAGO.map({1:"Pago", 0:"Pendente"})
    df['Valor'] = 816 / len(df)
    colunas = ["NOME","Status","Valor"]
    return df[colunas].copy().reset_index()

def cria_barras():
    bars = alt.Chart(dados).mark_bar().encode(
        x='Status',
        y='count(Status):Q',
        color=alt.Color('Status', scale=alt.Scale(scheme='tableau10'))
    ).properties(
        width=200,
        height=150,
        description='Detalhe Status'
    )

    chart = alt.vconcat(bars, data=dados, title="Pagamentos")
    st.altair_chart(chart, theme="streamlit", use_container_width=True)    

# =================================================================================================================================
# ===================================================== STREAMLIT COMPONENTS ======================================================
# =================================================================================================================================
st.set_page_config(page_title="Controle Assinatura",
                page_icon=":bar_chart:",
                layout="wide"
                )

colunas = ["NOME","Status","Valor"]
dados = busca_dados()[colunas]

# filtros para a tabela
st.sidebar.markdown('## Filtro para a tabela')

st.sidebar.header("Selecione uma opção aqui:")
status = st.sidebar.multiselect(
    "Selecione o Status desejado:",
    options=dados['Status'].unique(),
    default=dados['Status'].unique()
)

st.title('Controle Assinaturas :black_nib:')
st.write('Nesse projeto vamos analisar os pagamentos realizados de quem aderiu ao plano de assinatura para estudos.')
st.write(':zap::cool: Desenvolvido com :blue[Streamlit] e :red[Python] :heavy_check_mark::sunglasses::smile:')
st.markdown("##")

total_pago = int(dados[dados.Status == "Pago"].Valor.sum())
total_pendente = int(dados[dados.Status == "Pendente"].Valor.sum())
total_assinatura = int(dados.Valor.sum())

esquerda, centro, direita = st.columns(3)

with esquerda:
    st.subheader("Assinatura Total")
    st.subheader(f"R$ {total_assinatura:,}")
with centro:
    st.subheader("Total Pago")
    st.subheader(f"R$ {total_pago:,}")
with direita:
    st.subheader("Total Pendente")
    st.subheader(f"R$ {total_pendente:,}")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.header("Detalhamento")
    df_situacao = dados.query('Status == @status')
    
    st.table(df_situacao[colunas])

with col2:
    st.header("Resumo da Situação")
    df_grouped = dados.groupby("Status")["Valor"].sum()

    #cria_barras()    
    
    pagamento_por_situacao = (
            dados.groupby("Status").count()[['Valor']].sort_values(by="Status", ascending=False)
    )

    fig_status = px.bar(
        pagamento_por_situacao,
        x="Valor",
        y=pagamento_por_situacao.index,
        orientation="h",
        title="<b>Status Pagamento</b>",
        color_discrete_sequence=["#0083B8"] * len(pagamento_por_situacao),
        #color='Valor',
        text_auto='.1s',
        template='plotly_white',
    )
    fig_status.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    fig_status.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))
    )

    st.plotly_chart(fig_status)
