# 🌱 AgroSearch - Motor de Busca Textual

O **AgroSearch** é um protótipo de motor de busca textual desenvolvido em **Python e Streamlit** como parte da disciplina de Tendências em Ciência da Computação.

O projeto foi desenvolvido para aplicar conceitos de **Recuperação de Informação e processamento textual**, explorando técnicas utilizadas para preparar, indexar e classificar documentos por relevância de acordo com uma consulta.

O sistema trabalha com uma coleção de documentos relacionados à agricultura. A partir de uma pesquisa realizada pelo usuário, os textos passam por etapas de pré-processamento, os termos são organizados em um índice invertido e os documentos são avaliados de acordo com sua relevância para a consulta.

Para isso, o AgroSearch utiliza técnicas como **TF-IDF** e **similaridade de cosseno**, permitindo representar os documentos numericamente, atribuir importância aos termos e comparar a consulta com o conteúdo disponível.

---

## 🎓 Contexto Acadêmico

- **Instituição:** UNIPÊ
- **Disciplina:** Tendências em Ciência da Computação
- **Professor:** Me. Ricardo Roberto de Lima
- **Projeto:** AgroSearch - Motor de Busca Textual

---

## 🎯 Objetivo

O objetivo do projeto é reunir, em uma única aplicação, conceitos fundamentais de **Recuperação de Informação e processamento textual**, permitindo visualizar as principais etapas envolvidas no funcionamento de um motor de busca.

Os principais conceitos implementados são:

1. **Pré-processamento textual**
   - Tokenização
   - Normalização
   - Remoção de stopwords
   - Stemming

2. **Índice invertido**
   - Estrutura responsável por relacionar cada termo aos documentos nos quais ele aparece.

3. **TF, DF, IDF e TF-IDF**
   - Métricas utilizadas para analisar a frequência e a importância dos termos dentro da coleção de documentos.

4. **Ranking por relevância**
   - Ordenação dos documentos de acordo com sua relação com a consulta realizada pelo usuário.

5. **Similaridade de cosseno**
   - Comparação entre a representação vetorial da consulta e dos documentos para medir o grau de similaridade entre eles.

A aplicação também possui uma interface desenvolvida com **Streamlit**, permitindo acompanhar de forma didática as diferentes etapas do processo de busca.

---

## 🔎 Funcionamento

O fluxo principal do AgroSearch é:

```text
Documentos
    ↓
Pré-processamento textual
    ↓
Tokenização, normalização,
remoção de stopwords e stemming
    ↓
Índice invertido
    ↓
Consulta do usuário
    ↓
Pré-processamento da consulta
    ↓
TF / DF / IDF / TF-IDF
    ↓
Cálculo de relevância
    ↓
Ranking dos documentos
