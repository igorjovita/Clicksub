import streamlit as st

from database import DataBaseMysql
from functions import Functions

db = DataBaseMysql()
repo = Functions(db)


def lancamentos():
    st.write('''<style>

    [data-testid="column"] {
        width: calc(33.3333% - 1rem) !important;
        flex: 1 1 calc(33.3333% - 1rem) !important;
        min-width: calc(33% - 1rem) !important;
    }

    </style>''', unsafe_allow_html=True)

    staff = [st.session_state["name"]]
    id_staff = repo.select_id_staff(staff[0])
    select_operadoras = repo.select_operadoras()
    operadoras = []
    for item in select_operadoras:
        operadoras.append(item[1])

    with st.form('Lancamento_foto'):
        st.subheader('Lançamentos')

        col1, col2 = st.columns(2)
        with col1:
            data = st.date_input('Selecione a data', format='DD/MM/YYYY')
            operadora = st.selectbox('Selecione a Operadora', operadoras, index=None)
            video = st.text_input('Quantidade de Videos')

        with col2:
            nome_staff = st.selectbox('Selecione o staff', staff)
            fotos = st.text_input('Quantidade de Fotos')

        with st.expander('Lançar outra operadora'):
            colu1, colu2 = st.columns(2)

            with colu1:
                operadora2 = st.selectbox('Operadora secundaria', operadoras, index=None)
                video2 = st.text_input('Videos 2 operação')
            with colu2:
                fotos2 = st.text_input('Fotos 2 operação')

        if st.form_submit_button('Lançar no Sistema'):
            index = operadoras.index(operadora)
            id_operadora = select_operadoras[index][0]

            if operadora2:
                index = operadoras.index(operadora2)
                id_operadora2 = select_operadoras[index][0]

                repo.insert_click_lancamentos(data, id_staff, id_operadora, fotos, video, 'Pendente')
                repo.insert_click_lancamentos(data, id_staff, id_operadora2, fotos2, video2, 'Pendente')

            else:
                repo.insert_click_lancamentos(data, id_staff, id_operadora, fotos, video, 'Pendente')

            st.success('Lançamento registrado no sistema!')


