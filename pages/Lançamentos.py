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

if st.button('Lançar no Sistema'):

    st.write(data, nome_staff, fotos, video)

