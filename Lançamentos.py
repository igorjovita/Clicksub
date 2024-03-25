import streamlit as st


def lancamentos():
    st.write('''<style>

    [data-testid="column"] {
        width: calc(33.3333% - 1rem) !important;
        flex: 1 1 calc(33.3333% - 1rem) !important;
        min-width: calc(33% - 1rem) !important;
    }

    </style>''', unsafe_allow_html=True)

    staffs = ['Diego', 'Cauã', 'Thiago']
    operadoras = ['AcquaWorld', 'Seaquest', 'Pl Divers']

    with st.form('Lancamento_foto'):
        st.subheader('Lançamentos')

        col1, col2 = st.columns(2)
        with col1:
            data = st.date_input('Selecione a data', format='DD/MM/YYYY')
            operadora = st.selectbox('Selecione a Operadora', operadoras, index=None)
            video = st.text_input('Quantidade de Videos')

        with col2:
            nome_staff = st.selectbox('Selecione o staff', staffs, index=None)
            fotos = st.text_input('Quantidade de Fotos')

        with st.expander('Lançar outra operadora'):
            colu1, colu2 = st.columns(2)

            with colu1:
                operadora2 = st.selectbox('Operadora secundaria', operadoras, index=None)
                video2 = st.text_input('Videos 2 operação')
            with colu2:
                fotos2 = st.text_input('Fotos 2 operação')


        if st.form_submit_button('Lançar no Sistema'):

            if operadora2:

                st.write(data, nome_staff, operadora, fotos, video, operadora2, fotos2, video2)

            else:
                st.write(data, nome_staff, operadora, fotos, video)
