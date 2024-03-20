import streamlit as st

st.subheader('Lançamentos')

staffs = ['Diego', 'Cauã', 'Thiago']
operadoras = ['AcquaWorld', 'Seaquest', 'Pl Divers']

data = st.date_input('Selecione a data', format='DD/MM/YYYY')
nome_staff = st.selectbox('Selecione o staff', staffs, index=None)
operadora = st.selectbox('Selecione a Operadora', operadoras, index=None)

fotos = st.text_input('Quantidade de Fotos')
video = st.text_input('Quantidade de Videos')

if st.button('Lançar no Sistema'):

    st.write(data, nome_staff, fotos, video)

