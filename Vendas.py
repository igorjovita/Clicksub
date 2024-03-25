import time

import streamlit as st
import pandas as pd
from functions import select_planilha_acqua, pressionar, update_telefone, insert_clicksub, \
    select_titular, select_reserva_titular, update_foto_reserva


def layout_vendas():
    if 'botao' not in st.session_state:
        st.session_state.botao = False

    if 'lista_pagamento' not in st.session_state:
        st.session_state.lista_pagamento = []

    st.header('Controle de vendas')
    st.subheader('AcquaWorld')

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
                    pacote = st.selectbox('Pacotes', ['FOTO 5', 'FOTO 10', 'VIDEO', 'FOTO + VIDEO'], index=None,
                                          key=f'{reserva[0]} - pac')

                with col3:
                    pagamento = st.selectbox('Forma Pagamento', ['Dinheiro', 'Pix', 'Debito'], index=None,
                                             key=f'{reserva[0]} - pag')

                with col4:
                    valor = st.text_input('Valor', key=f'{reserva[0]} - valor')

                if telefone == reserva[1]:
                    telefone = ''

                if pacote is not None and pagamento is not None and valor is not None:
                    inputs[reserva[0]] = {'telefone': telefone, 'pacote': pacote, 'pagamento': pagamento,
                                          'valor': valor, 'id_reserva': reserva[3], 'id_cliente': reserva[4]}

                st.write('---')

            if st.form_submit_button(f'Lançar Pagamento'):

                st.write(inputs)

                for nome, valores in inputs.items():
                    telefone = valores['telefone']
                    pacote = valores['pacote']
                    pagamento = valores['pagamento']
                    valor = valores['valor']
                    id_reserva = valores['id_reserva']
                    id_cliente = valores['id_cliente']

                    if telefone != '':
                        update_telefone(id_cliente, telefone)

                    insert_clicksub(id_reserva, pacote, pagamento, valor)

                    update_foto_reserva(id_reserva, pacote)

                st.success('Pagamento Lançado')

                st.session_state.botao = False

                time.sleep(1.5)
                st.rerun()
