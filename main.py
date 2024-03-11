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

        for i, cliente in enumerate(clientes):
            col1, col2, col3, col4 = st.columns(4)
            tipo = st.session_state.df_state.loc[
                st.session_state.df_state['Nome'] == cliente, 'Tipo'].to_string(index=False)


            st.subheader(f'{cliente} - {tipo}')


            with col1:
                telefone_coluna = st.session_state.df_state.loc[
                    st.session_state.df_state['Nome'] == cliente, 'Telefone'].to_string(index=False)
                st.text_input('Telefone', telefone_coluna)



            with col2:
                pacote = st.selectbox('Pacotes', ['FOTO 5', 'FOTO 10', 'VIDEO', 'FOTO + VIDEO'], index=None,
                                      key=f'Pacote {i}')



            with col3:
                pagamento = st.selectbox('Forma Pagamento', ['Dinheiro', 'Pix', 'Debito'], index=None,
                                         key=f'Pagamento {i}')

            with col4:
                valor = 0

                if pagamento == 'Debito':
                    valor += 5

                if pacote == 'FOTO 5':
                    valor += 70

                elif pacote == 'FOTO 10':
                    valor += 80

                elif pacote == 'VIDEO':
                    valor += 90

                elif pacote == 'FOTO + VIDEO':
                    valor += 160

                st.text_input('Valor', valor, key=f'Valor {i}')






