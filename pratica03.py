# Aula 3: TF-IDF
# Prática: Calculadora Interativa de TF-IDF
# Objetivo: O usuário fornece uma Consulta (Query) e alguns Documentos. O app calcula o TF, o IDF e o TF-IDF final, exibindo os resultados em uma tabela, replicando o exemplo da página 19/20.



import streamlit as st
import math
import pandas as pd

st.title("📊 Calculadora de TF-IDF")

st.subheader("Coleção de Documentos")
docs_text = st.text_area("Um documento por linha:", 
                         value="o gato subiu no telhado\no cachorro correu no parque\no gato e o cachorro brincaram no parque", height=100)
query = st.text_input("Consulta (Query):", "gato")

if st.button("Calcular TF-IDF"):
    docs = [d.split() for d in docs_text.split("\n") if d]
    N = len(docs)
    
    # Frequência do termo na consulta
    tf_idf_results = []
    
    # Calcula DF(t)
    df_t = sum(1 for doc in docs if query.lower() in [w.lower() for w in doc])
    idf = math.log(N / df_t) if df_t > 0 else 0
    
    for i, doc in enumerate(docs):
        # TF(t, d)
        freq = doc.count(query.lower())
        tf = freq / len(doc) if len(doc) > 0 else 0
        
        # TF-IDF
        tfidf = tf * idf
        
        tf_idf_results.append({
            "Documento": f"Doc {i+1}",
            f"TF('{query}')": round(tf, 4),
            f"IDF('{query}')": round(idf, 4),
            "TF-IDF Final": round(tfidf, 4)
        })
        
    df_resposta = pd.DataFrame(tf_idf_results)
    st.dataframe(df_resposta, use_container_width=True)
    st.info(f"O termo '{query}' aparece em {df_t} de {N} documentos (DF). Logo, seu IDF é {round(idf, 4)}.")