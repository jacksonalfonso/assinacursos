import pandas as pd
import streamlit as st
import altair as alt
import plotly.express as px

@st.cache
def busca_dados(uploaded_file):
    # importando os dados
    if uploaded_file:
        origem = uploaded_file
    else:
        origem = 'controle.xlsx'

    df = pd.read_excel(origem, index_col=0)
    
    if not {'NOME', 'DATA', 'PAGO'}.issubset(df.columns):
        return pd.DataFrame()

    df['Status'] = df.PAGO.map({1:"Pago", 0:"Pendente"})
    df['Valor'] = 816 / len(df)
    return df.reset_index()

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

with st.expander("Upload Planilha"):
    uploaded_file = st.file_uploader("Fazer Upload da planilha de controle", type='xlsx')

#if  uploaded_file:
dados = busca_dados(uploaded_file)
#else:
#    dados = pd.DataFrame()
st.title('Controle Assinaturas :black_nib:  - SELECIONE UM ARQUIVO PARA VISUALIZAR')

if len(dados) > 0:
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
    qtde_pago = int(dados[dados.Status == "Pago"].NOME.count())
    
    total_pendente = int(dados[dados.Status == "Pendente"].Valor.sum())
    qtde_pendente = int(dados[dados.Status == "Pendente"].NOME.count())
    
    total_assinatura = int(dados.Valor.sum())
    total_assinantes = int(dados.NOME.count())

    esquerda, centro, direita = st.columns(3)

    with esquerda:
        st.subheader("Valor Assinatura")
        st.subheader(f"R$ {total_assinatura:,} \n (Qtde Assinantes: {total_assinantes}) ")
    with centro:
        st.subheader("Total Pago")
        st.subheader(f"R$ {total_pago:,} \n (Qtde Pagantes: {qtde_pago})")
    with direita:
        st.subheader("Total Pendente")
        st.subheader(f"R$ {total_pendente:,} \n (Qtde Pendente: {qtde_pendente})")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.header("Detalhamento")
        df_situacao = dados.query('Status == @status')
        colunas = ['NOME', 'Status', 'Valor']
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
            template='plotly_white',
        )
        fig_status.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
        fig_status.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=(dict(showgrid=False))
        )

        st.plotly_chart(fig_status)
