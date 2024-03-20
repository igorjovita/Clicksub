import streamlit as st

st.subheader('Lançamentos')

staffs = ['Diego', 'Cauã', 'Thiago']
operadoras = ['AcquaWorld', 'Seaquest', 'Pl Divers']

col1, col2, col3 = st.columns(3)

with col1:
    data = st.date_input('Selecione a data', format='DD/MM/YYYY')
    fotos = st.text_input('Quantidade de Fotos')

with col2:
    nome_staff = st.selectbox('Selecione o staff', staffs, index=None)
    video = st.text_input('Quantidade de Videos')

with col3:
    operadora = st.selectbox('Selecione a Operadora', operadoras, index=None)

with st.expander('Lançar outra operadora'):
    colu1, colu2, colu3 = st.columns(3)

    with colu1:
        operadora2 = st.selectbox('Selecione a Operadora secundaria', operadoras, index=None)

    with colu2:
        fotos2 = st.text_input('Quantidade de Fotos 2 operação')

    with colu3:
        video2 = st.text_input('Quantidade de Videos 2 operação')

if st.button('Lançar no Sistema'):

    if operadora2:

        st.write(data, nome_staff, operadora, fotos, video, operadora2, fotos2, video2)

    else:
        st.write(data, nome_staff, operadora, fotos, video)