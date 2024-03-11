import streamlit as st
import pandas as pd
from functions import select_planilha_acqua, pressionar

st.subheader('Click Sub')

if 'botao' not in st.session_state:
    st.session_state.botao = False

data_reserva = st.date_input('Data da panilha', format='DD/MM/YYYY')
if st.button('Pesquisar', on_click=pressionar):
    st.session_state.botao = True

state = st.session_state

if 'df_state' not in state:
    state.df_state = pd.DataFrame(columns=['Selecionar','Nome', 'Telefone', 'Comissario', 'Tipo', 'Fotos'])

if st.session_state.botao:

    dados = select_planilha_acqua(data_reserva)

    df = pd.DataFrame(dados, columns=['Nome', 'Telefone', 'Comissario', 'Tipo', 'Fotos'])

    df.insert(0, 'Selecionar', [False] * len(df))
    state.df_state = df

    state.df_state = st.data_editor(state.df_state, hide_index=True)

    if len(st.session_state.df_state.loc[st.session_state.df_state['Selecionar']]) > 0:
        st.write('---')
        clientes = (st.session_state.df_state.loc[st.session_state.df_state['Selecionar'], 'Nome']).tolist()

        for cliente in clientes:
            col1, col2, col3 = st.columns(3)

            with col1:
                st.text_input('Nome Cliente', value=cliente)

            with col2:
                telefone_coluna = st.session_state.df_state.loc[
                    st.session_state.df_state['Nome'] == cliente, 'Telefone']
                st.text_input('Telefone', telefone_coluna)

        st.write(clientes)







