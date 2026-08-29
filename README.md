# 🌱 AgroSearch - Motor de Busca Inteligente

O **AgroSearch** é um protótipo de motor de busca textual desenvolvido em **Python + Streamlit**, com o objetivo de aplicar conceitos de **Recuperação de Informação** e **Processamento Textual**.

O sistema trabalha com uma coleção de documentos relacionados à agricultura e permite que o usuário realize consultas textuais. A partir da consulta, o AgroSearch processa os textos, constrói um índice invertido, calcula a relevância dos documentos utilizando **TF-IDF** e apresenta um ranking do documento mais relevante para o menos relevante.

---

## 🎓 Contexto Acadêmico

- **Instituição:** UNIPÊ
- **Disciplina:** Tendências em Ciência da Computação
- **Professor:** Me. Ricardo Roberto de Lima
- **Projeto:** AgroSearch - Motor de Busca Inteligente

---

## 🎯 Objetivo

O objetivo do projeto é integrar, em uma única aplicação, os principais conceitos estudados nas práticas anteriores da disciplina:

1. Pré-processamento de texto;
2. Construção de Índice Invertido;
3. Cálculo de TF-IDF;
4. Ranqueamento de documentos;
5. Similaridade de Cosseno, como funcionalidade bônus.

A aplicação foi desenvolvida de forma didática, permitindo visualizar as diferentes etapas do processo de recuperação de informação.

---

## 🔎 Funcionamento

O fluxo principal do AgroSearch é:

```text
Documentos
    ↓
Pré-processamento
    ↓
Índice Invertido
    ↓
Consulta do usuário
    ↓
Pré-processamento da consulta
    ↓
TF / DF / IDF / TF-IDF
    ↓
Pontuação dos documentos
    ↓
Ranking por relevância
