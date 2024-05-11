import datetime
import time

import streamlit as st
import pandas as pd
from database import DataBaseMysql
from functions import Functions

db = DataBaseMysql()
repo = Functions(db)


def layout_vendas():
    st.write('''<style>

    [data-testid="column"] {
        width: calc(33.3333% - 1rem) !important;
        flex: 1 1 calc(33.3333% - 1rem) !important;
        min-width: calc(33% - 1rem) !important;
    }

    </style>''', unsafe_allow_html=True)
    if 'botao' not in st.session_state:
        st.session_state.botao = False

    if 'lista_pagamento' not in st.session_state:
        st.session_state.lista_pagamento = []

    st.header('Controle de vendas')
    st.subheader('AcquaWorld')

    data_reserva = st.date_input('Data da panilha', format='DD/MM/YYYY')

    select_titular = repo.select_titular(data_reserva)

    lista_titulares = []
    if select_titular is not None:
        for item in select_titular:
            lista_titulares.append(item[1])

    titular_reserva = st.selectbox('Escolha o titular da reserva', lista_titulares, index=None)

    if st.button('Pesquisar'):
        st.session_state.botao = True

    if st.session_state.botao:
        index = lista_titulares.index(titular_reserva)
        id_titular = select_titular[index][0]

        reservas_selecionadas = repo.select_reserva(data_reserva, id_titular)
        inputs = {}
        with st.form('Formulario'):
            for reserva in reservas_selecionadas:

                st.subheader(f'{reserva[0]} - {reserva[2]}')

                col1, col2 = st.columns(2)

                with col1:
                    telefone = st.text_input('Telefone', value=reserva[1], key=f'{reserva[0]} - tel')
                    pagamento = st.selectbox('Forma Pagamento', ['Dinheiro', 'Pix', 'Debito'], index=None,
                                             key=f'{reserva[0]} - pag')
                with col2:
                    pacote = st.selectbox('Pacotes', ['FOTO 5', 'FOTO 10', 'VIDEO', 'FOTO + VIDEO'], index=None,
                                          key=f'{reserva[0]} - pac')
                    valor = st.text_input('Valor', key=f'{reserva[0]} - valor')

                if telefone == reserva[1]:
                    telefone = ''

                if pacote is not None and pagamento is not None and valor is not None:
                    inputs[reserva[0]] = {'telefone': telefone, 'pacote': pacote, 'pagamento': pagamento,
                                          'valor': valor, 'id_reserva': reserva[3], 'id_cliente': reserva[4]}

                st.write('---')

            if st.form_submit_button(f'Lançar Pagamento'):
                data = datetime.datetime.today()
                st.write(inputs)

                for nome, valores in inputs.items():
                    telefone = valores['telefone']
                    pacote = valores['pacote']
                    pagamento = valores['pagamento']
                    valor = valores['valor']
                    id_reserva = valores['id_reserva']
                    id_cliente = valores['id_cliente']

                    if telefone != '':
                        repo.update_telefone(telefone, id_cliente)

                    repo.insert_click_pagamentos(data, id_reserva, pacote, pagamento, valor)

                    repo.update_foto_reserva(pacote, id_reserva)

                st.success('Pagamento Lançado')

                st.session_state.botao = False

                time.sleep(1.5)
                st.rerun()
