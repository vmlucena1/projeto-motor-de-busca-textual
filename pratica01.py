# Aula 1: Evolução da RI e Índices Invertidos
# Prática: Construtor Visual de Índice Invertido
# Objetivo: O usuário insere pequenos textos (simulando documentos) e o aplicativo constrói e exibe o índice invertido na tela, mostrando a transição do Índice Direto para o Invertido (como na página 05 do material).


import streamlit as st
from collections import defaultdict

st.title("🔗 Construtor de Índice Invertido")
st.markdown("Insira documentos (um por linha) para ver como o sistema cria o mapeamento **Termo -> Documentos**.")

documentos_input = st.text_area("Cole seus documentos aqui (1 por linha):", 
                                value="O gato correu\nO cachorro late\nO gato e o cachorro dormem",
                                height=150)

if st.button("Gerar Índice Invertido"):
    docs = [doc.strip() for doc in documentos_input.split("\n") if doc.strip()]
    
    # Índice Direto
    indice_direto = {f"Doc{i+1}": doc.split() for i, doc in enumerate(docs)}
    
    # Índice Invertido
    indice_invertido = defaultdict(list)
    for id_doc, termos in indice_direto.items():
        for termo in termos:
            if id_doc not in indice_invertido[termo.lower()]:
                indice_invertido[termo.lower()].append(id_doc)
                
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Índice Direto (Doc -> Termos)")
        st.json(indice_direto)
        
    with col2:
        st.subheader("Índice Invertido (Termo -> Docs)")
        st.json(dict(indice_invertido))
        
    st.success("Perceba como a busca por um termo específico fica muito mais rápida no índice da direita!")