import streamlit as st
import pandas as pd
from functions import select_planilha_acqua, pressionar

st.subheader('Click Sub')

if 'botao' not in st.session_state:
    st.session_state.botao = False

data_reserva = st.date_input('Data da panilha', format='DD/MM/YYYY')
if st.button('Pesquisar', on_click=pressionar):
    st.session_state.botao = True

if st.session_state.botao:

    dados = select_planilha_acqua(data_reserva)

    df = pd.DataFrame(dados, columns=['Nome', 'Telefone', 'Comissario', 'Tipo', 'Fotos'])

    df.insert(0, 'Selecionar', [False] * len(df))

    st.data_editor(df, hide_index=True)

    if len(st.session_state.df_state.loc[st.session_state.df_state['Selecionar']]) > 0:
        st.write('---')
        cliente = st.session_state.df_state.loc[st.session_state.df_state['Selecionar'], 'Nome']

        st.write(cliente)







