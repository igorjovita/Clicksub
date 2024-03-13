import streamlit as st
import pandas as pd
from functions import select_planilha_acqua, pressionar, update_telefone, insert_clicksub, \
    select_titular, select_reserva_titular

st.subheader('Click Sub')

if 'botao' not in st.session_state:
    st.session_state.botao = False

if 'lista_pagamento' not in st.session_state:
    st.session_state.lista_pagamento = []

data_reserva = st.date_input('Data da panilha', format='DD/MM/YYYY')

lista_titulares, nome_id_titular = select_titular(data_reserva)

titular_reserva = st.selectbox('Escolha o titular da reserva', lista_titulares, index=None)

if st.button('Pesquisar'):
    st.session_state.botao = True

id_titular = ''

if st.session_state.botao:
    for cliente in nome_id_titular:
        if cliente[0] == titular_reserva:
            id_titular = cliente[1]

    reservas_selecionadas = select_reserva_titular(data_reserva, id_titular)

    inputs = {}
    with st.form('Formulario'):
        for reserva in reservas_selecionadas:

            st.subheader(f'{reserva[0]} - {reserva[2]}')

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                telefone = st.text_input('Telefone', value=reserva[1], key=f'{reserva[0]} - tel')

            with col2:
                pacote = st.selectbox('Pacotes', ['FOTO 5', 'FOTO 10', 'VIDEO', 'FOTO + VIDEO'], index=None, key=f'{reserva[0]} - pac')

            with col3:
                pagamento = st.selectbox('Forma Pagamento', ['Dinheiro', 'Pix', 'Debito'], index=None, key=f'{reserva[0]} - pag')

            with col4:
                valor = st.text_input('Valor', key=f'{reserva[0]} - valor')

            inputs[reserva[0]] = {'telefone': telefone, 'pacote': pacote, 'pagamento': pagamento, 'valor': valor}

            st.write('---')

        if st.form_submit_button('Lançar Pagamento'):
            st.write(inputs)
            st.success('Pagamento Lançado')




# dados = select_planilha_acqua(data_reserva)
#
# if st.button('Pesquisar', on_click=pressionar):
#     st.session_state.botao = True
#
# state = st.session_state
#
# if 'df_state' not in state:
#     state.df_state = pd.DataFrame(
#         columns=['Selecionar', 'ID', 'Id reserva', 'Nome', 'Telefone', 'Comissario', 'Tipo', 'Fotos'])
#
# if st.session_state.botao:
#
#     df = pd.DataFrame(dados, columns=['ID', 'Id reserva', 'Nome', 'Telefone', 'Comissario', 'Tipo', 'Fotos'])
#
#     df.insert(0, 'Selecionar', [False] * len(df))
#     df_sem_id_reserva = df.drop(columns=['Id reserva'])
#     state.df_state = df_sem_id_reserva
#
#     st.session_state.df_state.set_index('ID', inplace=True)
#
#     state.df_state = st.data_editor(state.df_state, hide_index=True)
#
#     if len(st.session_state.df_state.loc[st.session_state.df_state['Selecionar']]) > 0:
#         st.write('---')
#         clientes = (st.session_state.df_state.loc[st.session_state.df_state['Selecionar'], 'Nome']).tolist()
#
#         for i, cliente in enumerate(clientes):
#
#             tipo = st.session_state.df_state.loc[
#                 st.session_state.df_state['Nome'] == cliente, 'Tipo'].values[0]
#
#             with st.form(f'{cliente} Foto'):
#
#
#                 st.subheader(f'{cliente} - {tipo}')
#
#                 col1, col2, col3, col4 = st.columns(4)
#
#                 with col1:
#                     telefone_coluna = st.session_state.df_state.loc[
#                         st.session_state.df_state['Nome'] == cliente, 'Telefone'].values[0]
#                     telefone = st.text_input('Telefone', telefone_coluna)
#
#                 with col2:
#                     pacote = st.selectbox('Pacotes', ['FOTO 5', 'FOTO 10', 'VIDEO', 'FOTO + VIDEO'], index=None,
#                                           key=f'Pacote {i}')
#
#                 with col3:
#                     pagamento = st.selectbox('Forma Pagamento', ['Dinheiro', 'Pix', 'Debito'], index=None,
#                                              key=f'Pagamento {i}')
#
#                 with col4:
#                     valor = st.text_input('Valor', key=f'Valor {i}')
#
#                 if st.form_submit_button('Lançar Pagamento'):
#
#                     id_cliente = st.session_state.df_state.loc[st.session_state.df_state['Nome'] == cliente].index[
#                         0]
#
#                     if telefone != telefone_coluna:
#                         st.write(telefone)
#                         st.write(cliente)
#                         update_telefone(id_cliente, telefone)
#
#                     id_reserva = int(df.loc[df['Nome'] == cliente, 'Id reserva'].values[0])
#
#                     insert_clicksub(id_reserva, pacote, pagamento, valor)
#                     update_foto_reserva(id_reserva, pacote)

