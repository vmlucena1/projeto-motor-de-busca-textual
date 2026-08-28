# AgroSearch.py
# Motor de Busca Inteligente para AgroTech Solutions
# Projeto Acadêmico — Recuperação de Informação e PLN
#
# Relação com as Práticas do Professor:
#   Prática 01 → Seção 4 (Índice Invertido)
#   Prática 02 → Seção 3 (Pipeline de Pré-processamento)
#   Prática 03 → Seções 6 e 7 (Calculadora TF-IDF)
#   Desafio Bônus → Seção 9 (Similaridade de Cosseno)

import streamlit as st
import re
import unicodedata
import math
import pandas as pd
from collections import defaultdict


# ============================================================
# BASE DE DOCUMENTOS — cadastrados diretamente no código
# ============================================================
documentos = {
    "Doc 1": "A soja requer irrigação constante durante o período de floração para garantir a produtividade.",
    "Doc 2": "O controle biológico de lagartas na soja pode ser feito com a vespa Trichogramma.",
    "Doc 3": "A adubação verde com leguminosas melhora o nitrogênio no solo para o milho.",
    "Doc 4": "Lagartas desfolhadoras causam grande prejuízo na cultura da soja e do algodão.",
    "Doc 5": "A irrigação por gotejamento economiza água e é ideal para o cultivo orgânico.",
}


# ============================================================
# STOPWORDS EM PORTUGUÊS — lista manual, sem biblioteca externa
# ============================================================
# Após normalização, palavras com acento perdem o acento.
# Ex.: "é" → "e", "são" → "sao", "não" → "nao"
STOPWORDS = {
    # Artigos
    "a", "o", "os", "as",
    # Preposições e contrações
    "de", "da", "do", "das", "dos",
    "em", "na", "no", "nas", "nos",
    "para", "por", "com",
    "ao", "aos",
    "pelo", "pela", "pelos", "pelas",
    # Conjunções
    "e", "ou", "mas", "que", "se",
    # Artigos indefinidos
    "um", "uma", "uns", "umas",
    # Verbos auxiliares/copulativos
    "ser", "sao", "foi", "era",
    # Pronomes
    "seu", "sua", "seus", "suas",
    "ele", "ela", "eles", "elas",
    "esse", "essa", "esses", "essas",
    "este", "esta", "estes", "estas",
    "isso", "isto",
    # Alta frequência / baixo valor semântico
    "nao", "mais", "muito", "bem", "ja",
    "pode", "podem", "tem",
}


# ============================================================
# FUNÇÕES DE PRÉ-PROCESSAMENTO
# (Inspirado na Prática 02 do professor)
# ============================================================

def normalizar_texto(texto: str) -> str:
    """
    Normalização: converte para minúsculas e remove acentos.
    Usa NFD + encode ASCII para eliminar diacríticos.
    Ex.: "Irrigação" → "irrigacao"
    """
    texto = texto.lower()
    texto = unicodedata.normalize('NFD', texto).encode('ascii', 'ignore').decode('utf-8')
    return texto


def stemmer_simples(palavra: str) -> str:
    """
    Stemming rudimentar: remove sufixos comuns do português.
    Só aplica o corte se o radical resultante tiver >= 4 caracteres
    para evitar truncamentos que destruam a palavra.
    Ex.: "irrigacao" → "irriga", "lagartas" → "lagarta"
    """
    # Sufixos em ordem do mais longo para o mais curto (evita matches parciais)
    sufixos = [
        "amento", "amentos", "imento", "imentos",
        "mente",
        "coes",           # normalização de "ções"
        "cao",            # normalização de "ção"
        "doras", "dora", "dores", "dor",
        "osas", "osos", "osa", "oso",
        "adas", "ados", "ada", "ado",
        "ando", "endo", "indo",
        "ores", "or",
        "veis", "vel",
        "uras", "ura",
        "agem", "agens",
        "icas", "icos", "ica", "ico",
        "ais", "al",
    ]
    for sufixo in sufixos:
        if palavra.endswith(sufixo):
            radical = palavra[:-len(sufixo)]
            if len(radical) >= 4:
                return radical
    # Regra final: remove 's' plural apenas em palavras com 5+ caracteres
    if len(palavra) > 4 and palavra.endswith('s'):
        return palavra[:-1]
    return palavra


def preprocessar(texto: str, usar_stopwords: bool = True, usar_stemming: bool = True) -> list:
    """
    Pipeline completo de pré-processamento — 4 etapas:
      1. Tokenização  → separa palavras com regex
      2. Normalização → minúsculas + sem acentos
      3. Stopwords    → remove termos sem valor semântico (se ativado)
      4. Stemming     → reduz à raiz (se ativado)
    """
    # Etapa 1: Tokenização
    tokens = re.findall(r'\b\w+\b', texto)

    # Etapa 2: Normalização
    tokens = [normalizar_texto(t) for t in tokens]

    # Etapa 3: Remoção de Stopwords
    if usar_stopwords:
        tokens = [t for t in tokens if t not in STOPWORDS]

    # Etapa 4: Stemming
    if usar_stemming:
        tokens = [stemmer_simples(t) for t in tokens]

    return tokens


# ============================================================
# ÍNDICE INVERTIDO — implementação manual
# (Inspirado na Prática 01 do professor)
# ============================================================

def construir_indice_invertido(docs_processados: dict) -> dict:
    """
    Constrói o índice invertido: Termo → [lista de IDs de documentos].
    Utiliza defaultdict(list) e garante que cada documento apareça
    no máximo uma vez por termo.
    Resultado final ordenado alfabeticamente por termo.
    """
    indice = defaultdict(list)
    for id_doc, tokens in docs_processados.items():
        for token in tokens:
            if id_doc not in indice[token]:
                indice[token].append(id_doc)
    return dict(sorted(indice.items()))


# ============================================================
# CÁLCULOS TF-IDF — implementação manual, sem scikit-learn
# (Inspirado na Prática 03 do professor)
# ============================================================

def calcular_tf(termo: str, tokens_doc: list) -> float:
    """
    TF(t, d) = frequência de t em d  ÷  total de tokens de d.
    Mede a importância do termo dentro do documento.
    """
    if not tokens_doc:
        return 0.0
    return tokens_doc.count(termo) / len(tokens_doc)


def calcular_df(termo: str, docs_processados: dict) -> int:
    """
    DF(t) = número de documentos que contêm o termo t.
    """
    return sum(1 for tokens in docs_processados.values() if termo in tokens)


def calcular_idf(termo: str, docs_processados: dict) -> float:
    """
    IDF(t) = ln(N / DF(t)).
    Penaliza termos muito comuns na coleção (baixo poder discriminativo).
    Retorna 0 quando DF = 0 para evitar divisão por zero.
    """
    N = len(docs_processados)
    df = calcular_df(termo, docs_processados)
    return math.log(N / df) if df > 0 else 0.0


def calcular_ranking(query_tokens: list, docs_processados: dict) -> tuple:
    """
    Para cada termo da query e cada documento, calcula TF, DF, IDF e TF-IDF.
    Score do documento = soma dos TF-IDF de todos os termos da query.
    Retorna:
      - ranking: lista de (id_doc, score) ordenada do maior para o menor score
      - detalhes: lista de dicts com todas as métricas para exibição didática
    """
    scores = {id_doc: 0.0 for id_doc in docs_processados}
    detalhes = []

    for termo in query_tokens:
        df = calcular_df(termo, docs_processados)
        idf = calcular_idf(termo, docs_processados)

        for id_doc, tokens_doc in docs_processados.items():
            tf = calcular_tf(termo, tokens_doc)
            tfidf = tf * idf
            scores[id_doc] += tfidf
            detalhes.append({
                "Termo": termo,
                "Documento": id_doc,
                "Frequência": tokens_doc.count(termo),
                "TF": round(tf, 6),
                "DF": df,
                "IDF": round(idf, 6),
                "TF-IDF": round(tfidf, 6),
            })

    ranking = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return ranking, detalhes


# ============================================================
# SIMILARIDADE DE COSSENO — implementação manual (Bônus)
# ============================================================

def calcular_vetor_tfidf(tokens_alvo: list, vocabulario: list, docs_processados: dict) -> dict:
    """
    Calcula o vetor TF-IDF de tokens_alvo no espaço do vocabulário.
    O IDF é sempre calculado com base no corpus de documentos (docs_processados),
    independente de tokens_alvo ser um documento ou uma query.
    """
    n = len(tokens_alvo)
    vetor = {}
    for termo in vocabulario:
        tf = tokens_alvo.count(termo) / n if n > 0 else 0.0
        idf = calcular_idf(termo, docs_processados)
        vetor[termo] = tf * idf
    return vetor


def produto_escalar(v1: dict, v2: dict) -> float:
    """Produto escalar de dois vetores representados como dicionários."""
    return sum(v1.get(k, 0.0) * v2.get(k, 0.0) for k in v1)


def norma_vetor(v: dict) -> float:
    """Norma euclidiana (L2) de um vetor representado como dicionário."""
    return math.sqrt(sum(val ** 2 for val in v.values()))


def calcular_similaridade_cosseno(vetor_query: dict, vetor_doc: dict) -> float:
    """
    Similaridade de Cosseno = produto_escalar(q, d) / (norma(q) × norma(d)).
    Retorna 0 quando algum dos vetores é nulo (evita divisão por zero).
    """
    pe = produto_escalar(vetor_query, vetor_doc)
    nq = norma_vetor(vetor_query)
    nd = norma_vetor(vetor_doc)
    if nq == 0.0 or nd == 0.0:
        return 0.0
    return pe / (nq * nd)


# ============================================================
# INTERFACE STREAMLIT — aplicação de página única
# ============================================================

st.set_page_config(
    page_title="AgroSearch",
    page_icon="🌱",
    layout="wide",
)

# — Cabeçalho —
st.title("🌱 AgroSearch - Motor de Busca Inteligente")
st.markdown("**Recuperação de Informação e Processamento de Linguagem Natural**")
st.caption("AgroTech Solutions — Protótipo Acadêmico")
st.divider()


# ============================================================
# SEÇÃO 1 — BASE DE DOCUMENTOS
# ============================================================
st.subheader("📚 Seção 1 — Base de Documentos")
st.markdown(
    "Os cinco documentos abaixo compõem a coleção da **AgroTech Solutions** "
    "e estão cadastrados diretamente no código — sem uploads ou banco de dados."
)

cols_docs = st.columns(2)
for i, (id_doc, texto) in enumerate(documentos.items()):
    with cols_docs[i % 2]:
        with st.expander(f"📄 {id_doc}", expanded=False):
            st.write(texto)

st.divider()


# ============================================================
# SEÇÃO 2 — CONFIGURAÇÕES DE PRÉ-PROCESSAMENTO
# ============================================================
st.subheader("⚙️ Seção 2 — Configurações de Pré-processamento")
st.markdown(
    "Altere os checkboxes abaixo para ver o impacto em tempo real no vocabulário, "
    "no índice invertido e nos resultados da busca."
)

col_sw, col_st = st.columns(2)
with col_sw:
    usar_stopwords = st.checkbox(
        "🗑️ Remover Stopwords",
        value=True,
        help="Remove palavras sem valor semântico: artigos, preposições, conjunções etc.",
    )
with col_st:
    usar_stemming = st.checkbox(
        "✂️ Aplicar Stemming",
        value=True,
        help="Reduz palavras à raiz removendo sufixos comuns do português.",
    )

# — Processamento dinâmico — recalcula tudo ao mudar um checkbox —
docs_processados = {
    id_doc: preprocessar(texto, usar_stopwords, usar_stemming)
    for id_doc, texto in documentos.items()
}

vocabulario = sorted(set(t for tokens in docs_processados.values() for t in tokens))

st.divider()


# ============================================================
# SEÇÃO 3 — PIPELINE DE PRÉ-PROCESSAMENTO
# ============================================================
st.subheader("🔬 Seção 3 — Pipeline de Pré-processamento")
st.info(
    "Cada documento passa pelo pipeline: "
    "**Tokenização → Normalização → Stopwords → Stemming**. "
    "O resultado são os tokens que alimentam o índice invertido e o TF-IDF."
)

tabela_pipeline = [
    {
        "Documento": id_doc,
        "Texto Original": documentos[id_doc],
        "Tokens Processados": " | ".join(tokens) if tokens else "(vazio)",
        "Nº de Tokens": len(tokens),
    }
    for id_doc, tokens in docs_processados.items()
]
st.dataframe(pd.DataFrame(tabela_pipeline), use_container_width=True)

col_m1, col_m2 = st.columns([1, 3])
with col_m1:
    st.metric("📖 Termos no vocabulário", len(vocabulario))
with col_m2:
    with st.expander("🔎 Ver lista completa do vocabulário"):
        st.write(", ".join(vocabulario) if vocabulario else "Vocabulário vazio.")

st.divider()


# ============================================================
# SEÇÃO 4 — ÍNDICE INVERTIDO
# ============================================================
st.subheader("🗂️ Seção 4 — Índice Invertido")
st.markdown(
    "O índice invertido mapeia **Termo → Documentos**. "
    "Permite encontrar documentos relevantes sem percorrer toda a coleção. "
    "A coluna **DF** (Document Frequency) indica em quantos documentos o termo aparece."
)

indice_invertido = construir_indice_invertido(docs_processados)

if indice_invertido:
    tabela_indice = [
        {
            "Termo": termo,
            "Documentos": ", ".join(docs),
            "DF": len(docs),
        }
        for termo, docs in indice_invertido.items()
    ]
    st.dataframe(pd.DataFrame(tabela_indice), use_container_width=True)

    with st.expander("🔍 Ver índice invertido em formato JSON"):
        st.json(indice_invertido)
else:
    st.warning("Vocabulário vazio. Ajuste as configurações de pré-processamento.")

st.divider()


# ============================================================
# SEÇÃO 5 — CONSULTA (QUERY)
# ============================================================
st.subheader("🔎 Seção 5 — Consulta")
query_raw = st.text_input(
    "Digite sua consulta:",
    placeholder="Ex.: irrigação soja",
    help="Aceita uma ou várias palavras. A query passa pelo mesmo pipeline dos documentos.",
)

if query_raw.strip():
    # A query passa pelo mesmo pipeline de pré-processamento
    query_tokens = preprocessar(query_raw, usar_stopwords, usar_stemming)

    if query_tokens:
        st.markdown(f"**Tokens da query após pré-processamento:** `{query_tokens}`")
    else:
        st.warning(
            "⚠️ A query ficou vazia após o pré-processamento. "
            "Tente desativar Stopwords/Stemming ou use termos mais específicos."
        )

    if query_tokens:
        st.divider()

        # ============================================================
        # SEÇÕES 6 E 7 — CÁLCULO MANUAL DE TF-IDF
        # ============================================================
        st.subheader("📊 Seções 6 e 7 — Cálculo Manual de TF-IDF")
        st.markdown(
            "| Fórmula | Descrição |\n"
            "|---|---|\n"
            "| **TF(t, d)** = freq(t, d) / \\|d\\| | Frequência relativa do termo no documento |\n"
            "| **DF(t)** | Número de documentos que contêm o termo |\n"
            "| **IDF(t)** = ln(N / DF(t)) | Raridade do termo na coleção (N = total de docs) |\n"
            "| **TF-IDF(t, d)** = TF × IDF | Score final: importância do termo no documento |"
        )
        st.markdown(
            f"*N (total de documentos) = **{len(docs_processados)}***  |  "
            f"*Termos da query: {query_tokens}*"
        )

        ranking, detalhes = calcular_ranking(query_tokens, docs_processados)

        df_detalhes = pd.DataFrame(detalhes)

        with st.expander("📋 Tabela completa: todos os termos × todos os documentos", expanded=True):
            st.dataframe(df_detalhes, use_container_width=True)

        df_relevantes = df_detalhes[df_detalhes["Frequência"] > 0]
        if not df_relevantes.empty:
            with st.expander("✅ Filtrado: apenas linhas com Frequência > 0"):
                st.dataframe(df_relevantes, use_container_width=True)

        st.divider()

        # ============================================================
        # SEÇÃO 8 — RANKING POR TF-IDF
        # ============================================================
        st.subheader("🏆 Seção 8 — Ranking por TF-IDF")
        st.markdown(
            "**Score TF-IDF** de cada documento = soma dos TF-IDF de todos os termos da query naquele documento."
        )

        max_score = max(score for _, score in ranking) if ranking else 0.0

        if max_score == 0.0:
            st.warning(
                "⚠️ Nenhum documento relevante foi encontrado para os termos informados. "
                "Tente uma consulta diferente ou desative o Stemming / Stopwords."
            )
        else:
            melhor_doc, melhor_score = ranking[0]
            st.success(
                f"🏆 Documento mais relevante: **{melhor_doc}**  |  "
                f"Score TF-IDF: `{round(melhor_score, 6)}`"
            )
            st.markdown(f"> *{documentos[melhor_doc]}*")

            posicoes = ["🥇 1º", "🥈 2º", "🥉 3º", "4º", "5º"]
            tabela_ranking = [
                {
                    "Posição": posicoes[i] if i < len(posicoes) else f"{i + 1}º",
                    "Documento": id_doc,
                    "Score TF-IDF": round(score, 6),
                    "Texto": documentos[id_doc],
                }
                for i, (id_doc, score) in enumerate(ranking)
            ]
            st.dataframe(pd.DataFrame(tabela_ranking), use_container_width=True)

        st.divider()

        # ============================================================
        # SEÇÃO 9 — SIMILARIDADE DE COSSENO (BÔNUS)
        # ============================================================
        st.subheader("📐 Seção 9 — Similaridade de Cosseno (Bônus)")
        st.info(
            "**Ranking TF-IDF acumulado** (Seção 8): soma os scores TF-IDF de cada termo da query "
            "nos documentos. Reflete a importância dos termos consultados *dentro* de cada documento.\n\n"
            "**Similaridade de Cosseno** (esta seção): compara a *direção* dos vetores TF-IDF da query "
            "e dos documentos. Especialmente útil em consultas com múltiplas palavras, pois pondera "
            "o quanto os dois vetores 'apontam na mesma direção' no espaço vetorial."
        )

        # Espaço vetorial: união dos termos da query e do vocabulário dos documentos
        vocab_cosseno = sorted(set(query_tokens) | set(vocabulario))

        # Vetor TF-IDF da query (TF calculado sobre os tokens da query; IDF sobre o corpus)
        vetor_query = calcular_vetor_tfidf(query_tokens, vocab_cosseno, docs_processados)

        resultados_cosseno = []
        for id_doc, tokens_doc in docs_processados.items():
            vetor_doc = calcular_vetor_tfidf(tokens_doc, vocab_cosseno, docs_processados)
            sim = calcular_similaridade_cosseno(vetor_query, vetor_doc)
            resultados_cosseno.append({
                "Documento": id_doc,
                "Similaridade Cosseno": round(sim, 6),
                "Texto": documentos[id_doc],
            })

        resultados_cosseno.sort(key=lambda x: x["Similaridade Cosseno"], reverse=True)

        max_cos = resultados_cosseno[0]["Similaridade Cosseno"] if resultados_cosseno else 0.0

        if max_cos > 0.0:
            melhor_cos_doc = resultados_cosseno[0]["Documento"]
            st.success(
                f"📐 Documento mais similar (Cosseno): **{melhor_cos_doc}**  |  "
                f"Similaridade: `{resultados_cosseno[0]['Similaridade Cosseno']}`"
            )
        else:
            st.warning("⚠️ Similaridade de cosseno zero para todos os documentos com esta query.")

        st.dataframe(pd.DataFrame(resultados_cosseno), use_container_width=True)

else:
    st.info("💡 Digite uma consulta no campo acima para ver os resultados do motor de busca.")


# — Rodapé —
st.divider()
st.markdown(
    "<small>🌱 **AgroSearch** — Projeto Acadêmico de Recuperação de Informação | "
    "AgroTech Solutions (fictícia) | Implementação manual: sem scikit-learn</small>",
    unsafe_allow_html=True,
)
