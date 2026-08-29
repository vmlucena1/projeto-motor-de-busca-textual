# Aula 2: Busca Léxica e Pré-processamento
# Prática: Simulador de Pipeline de Pré-processamento
# Objetivo: Demonstrar passo a passo as 4 etapas citadas no material (Tokenização, Normalização, Remoção de Stopwords e Stemming rudimentar) usando expander do Streamlit.


import streamlit as st
import re
import unicodedata

st.title("🧹 Pipeline de Pré-processamento de Texto")
texto_bruto = st.text_input("Digite um texto:", "Os GATOS correram RAPIDAMENTE para o céu!")

# 1. Tokenização
tokens = re.findall(r'\b\w+\b', texto_bruto)

# 2. Normalização (Lowercase + Sem acentos)
def normalize(text):
    text = text.lower()
    text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode('utf-8')
    return text
tokens_norm = [normalize(t) for t in tokens]

# 3. Stopwords (Lista simples)
stopwords = ["os", "o", "a", "para", "de", "em"]
tokens_sem_stop = [t for t in tokens_norm if t not in stopwords]

# 4. Stemming Simulado (cortando sufixos comuns)
def stemmer_simples(palavra):
    if palavra.endswith("entos"): return palavra[:-4]
    if palavra.endswith("amente"): return palavra[:-5]
    if palavra.endswith("ados"): return palavra[:-3]
    return palavra
tokens_stem = [stemmer_simples(t) for t in tokens_sem_stop]

# Exibição do Pipeline
with st.expander("1. Tokenização", expanded=True):
    st.write(tokens)
with st.expander("2. Normalização (Minúsculas e Sem Acentos)"):
    st.write(tokens_norm)
with st.expander("3. Remoção de Stopwords"):
    st.write(tokens_sem_stop)
with st.expander("4. Stemming (Redução à raiz)"):
    st.write(tokens_stem)