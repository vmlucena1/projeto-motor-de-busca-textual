# AgroSearch.py
# Motor de Busca Inteligente
# Projeto Acadêmico - Recuperação de Informação e PLN
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
# BASE DE DOCUMENTOS - conteúdo completo dos PDFs, hardcoded
# ============================================================
documentos = {

    "Doc 1": (
        "A soja é uma cultura de grande importância econômica e alimentar, utilizada na produção de óleo, farelo, "
        "ração animal, biocombustíveis e diversos produtos industrializados. Para que a planta expresse seu potencial "
        "produtivo, fatores como fertilidade do solo, temperatura, luminosidade e disponibilidade de água precisam "
        "estar em equilíbrio. Entre esses fatores, a água ocupa posição central porque participa diretamente da "
        "fotossíntese, do transporte de nutrientes, da manutenção da temperatura dos tecidos e do crescimento das "
        "raízes, folhas, flores e vagens. Quando o solo não oferece umidade suficiente, a planta passa a economizar "
        "água, fecha parcialmente os estômatos e reduz sua atividade fotossintética. "
        "Durante a fase de floração, a soja entra em um estágio decisivo do ciclo produtivo. A planta continua "
        "crescendo, mas precisa direcionar energia para a formação e manutenção das flores. Parte dessas flores dará "
        "origem às vagens e, posteriormente, aos grãos. Nessa etapa, períodos de deficiência hídrica podem aumentar "
        "o abortamento de flores, limitar a formação de vagens e reduzir o número final de grãos por planta. Por "
        "isso, a manutenção de um suprimento hídrico regular é especialmente importante. "
        "Em áreas onde a chuva é insuficiente ou irregular, a irrigação funciona como uma ferramenta de segurança "
        "produtiva. O manejo deve considerar o tipo de solo, a profundidade efetiva das raízes, a fase de "
        "desenvolvimento da planta, a temperatura, a umidade do ar, o vento e a ocorrência de precipitações. Solos "
        "arenosos armazenam menos água e podem exigir irrigações mais frequentes, enquanto solos argilosos costumam "
        "reter água por mais tempo. "
        "A falta de água pode afetar a produtividade de várias formas: reduz a expansão foliar, pode provocar queda "
        "de flores e vagens jovens, e pode limitar o enchimento dos grãos. Um bom sistema de irrigação precisa "
        "fornecer água de maneira uniforme e no momento adequado. Aplicações excessivas representam desperdício de "
        "água e energia e podem provocar lixiviação de nutrientes. "
        "A soja pode ser irrigada por diferentes métodos. A aspersão por pivô central é bastante utilizada em áreas "
        "mecanizadas. O manejo da irrigação precisa ser analisado sob a perspectiva da sustentabilidade, pois a "
        "agricultura utiliza parcela significativa dos recursos hídricos disponíveis. Monitorar a umidade do solo, "
        "considerar a previsão de chuva e evitar aplicações em condições de elevada perda por evaporação aumentam "
        "a eficiência do sistema. Durante a floração, recomenda-se acompanhar com maior atenção as condições de "
        "umidade do solo e o estado das plantas. A disponibilidade adequada de água durante a floração é um dos "
        "elementos mais importantes para a estabilidade produtiva da soja e para uma produção mais sustentável."
    ),

    "Doc 2": (
        "A soja é uma das culturas agrícolas de maior importância econômica e, durante seu desenvolvimento, pode ser "
        "atacada por diferentes espécies de insetos-praga. Entre os problemas mais frequentes estão as lagartas que "
        "se alimentam das folhas, flores, vagens ou outras partes da planta. Quando presentes em níveis elevados, "
        "esses insetos reduzem a área foliar, prejudicam a fotossíntese e podem comprometer a formação e o "
        "enchimento dos grãos. Por essa razão, o monitoramento das populações de lagartas e a adoção de medidas de "
        "manejo são etapas fundamentais para preservar a produtividade da lavoura. "
        "O controle biológico consiste no uso ou na conservação de organismos capazes de reduzir populações de "
        "pragas. Esses organismos podem ser predadores, parasitoides ou microrganismos patogênicos. No caso das "
        "lagartas que atacam a soja, uma das alternativas é o emprego de pequenas vespas parasitoides do gênero "
        "Trichogramma. Elas fazem parte de um grupo de inimigos naturais utilizado em programas de manejo integrado "
        "de pragas porque atuam sobre uma fase muito inicial do ciclo do inseto-alvo: o ovo. "
        "As vespas de Trichogramma são diminutas e não são utilizadas para atacar diretamente lagartas já "
        "desenvolvidas. A fêmea localiza ovos de mariposas e deposita seus próprios ovos no interior deles. Em vez "
        "de nascer a lagarta da praga, desenvolve-se o parasitoide. Dessa forma, parte dos ovos presentes na "
        "lavoura deixa de originar novas lagartas, ajudando a reduzir a pressão da praga no início de sua geração. "
        "O uso de controle biológico deve estar associado ao acompanhamento da lavoura. A inspeção periódica permite "
        "identificar a presença de adultos, posturas e lagartas pequenas. O monitoramento também é importante porque "
        "a cultura da soja pode abrigar diferentes espécies de lagartas, e o manejo deve considerar qual inseto está "
        "presente, sua densidade e o estágio de desenvolvimento da cultura. "
        "O uso de Trichogramma apresenta melhor sentido agronômico quando faz parte de um programa de manejo "
        "integrado de pragas, o MIP. O produtor pode associar o controle biológico ao monitoramento, à escolha de "
        "cultivares, à conservação de inimigos naturais e, quando necessário, ao uso criterioso de produtos "
        "fitossanitários compatíveis. Uma vantagem do controle biológico é a possibilidade de atuar de maneira "
        "seletiva, contribuindo para a conservação da biodiversidade da lavoura e fortalecendo estratégias de "
        "agricultura sustentável. A eficiência de um programa com parasitoides depende também das condições "
        "encontradas no campo: aplicações de inseticidas não seletivos podem reduzir a sobrevivência dos agentes de "
        "controle biológico. O controle biológico de lagartas na soja com vespas do gênero Trichogramma baseia-se "
        "principalmente no parasitismo de ovos das pragas, contribuindo para reduzir a pressão de lagartas, "
        "preservar organismos benéficos e manter a produtividade da cultura da soja."
    ),

    "Doc 3": (
        "O milho apresenta elevada exigência nutricional e responde de forma significativa à disponibilidade de "
        "nitrogênio no solo. Esse nutriente participa da formação de proteínas, enzimas, clorofila e outros "
        "compostos essenciais ao crescimento vegetal. Quando o fornecimento de nitrogênio é insuficiente, as "
        "plantas podem apresentar menor desenvolvimento, folhas com coloração verde menos intensa, redução da área "
        "foliar e menor capacidade fotossintética. Em situações de deficiência acentuada, o potencial de formação "
        "de espigas e de enchimento de grãos pode ser comprometido, causando queda de produtividade. "
        "A adubação verde é uma prática agrícola baseada no cultivo de plantas destinadas principalmente à proteção "
        "e à melhoria das condições do solo. Essas espécies podem ser cultivadas antes da cultura principal, em "
        "rotação, sucessão ou consórcio. O objetivo não é apenas acrescentar nutrientes, mas também aumentar a "
        "matéria orgânica, proteger o solo contra erosão, favorecer a atividade biológica e contribuir para a "
        "ciclagem de elementos minerais. "
        "Entre as plantas utilizadas como adubo verde, as leguminosas têm destaque por sua capacidade de estabelecer "
        "associação simbiótica com bactérias fixadoras de nitrogênio. Essas bactérias, conhecidas como rizóbios, "
        "formam nódulos nas raízes de espécies compatíveis e conseguem transformar o nitrogênio atmosférico em "
        "formas que passam a integrar os tecidos vegetais. Esse processo é denominado fixação biológica de "
        "nitrogênio. Dessa maneira, parte do nitrogênio presente na biomassa da leguminosa tem origem no ar, e não "
        "apenas nas reservas minerais já existentes no solo. "
        "Quando o milho é implantado após uma leguminosa bem manejada, ele pode se beneficiar do nitrogênio "
        "proveniente da decomposição dos resíduos vegetais e da melhoria geral do ambiente do solo. A cultura "
        "sucessora não recebe todo o nitrogênio de uma só vez, pois a liberação depende da velocidade de "
        "decomposição da palhada, da relação entre carbono e nitrogênio dos resíduos, da temperatura, da umidade "
        "e da atividade dos microrganismos. "
        "A escolha da espécie utilizada como adubo verde deve considerar a região, o calendário agrícola, o clima "
        "e o tipo de solo. Plantas como crotalárias, mucunas, feijão-de-porco e guandu podem ser empregadas em "
        "diferentes sistemas. Os benefícios da adubação verde não se limitam ao nitrogênio: a presença de raízes "
        "e resíduos vegetais contribui para o aumento da matéria orgânica, favorece a agregação das partículas e "
        "ajuda a proteger a superfície contra o impacto das chuvas. Para aproveitar melhor o nitrogênio da "
        "adubação verde, é importante buscar sincronização entre a liberação dos nutrientes e a demanda do milho. "
        "A adubação verde com leguminosas pode melhorar a disponibilidade e a ciclagem de nitrogênio no solo e "
        "criar condições favoráveis para o milho cultivado em sequência, sendo uma estratégia associada à "
        "agricultura conservacionista e ao uso mais eficiente dos recursos."
    ),

    "Doc 4": (
        "As lagartas desfolhadoras estão entre as pragas de maior importância econômica em diferentes sistemas de "
        "produção agrícola. Na soja e no algodão, elas se alimentam principalmente das folhas, reduzindo a área "
        "foliar disponível para a realização da fotossíntese. Quando a infestação ocorre de forma intensa ou em "
        "momentos críticos do desenvolvimento das plantas, a perda de folhas pode comprometer a produção de energia, "
        "a formação de estruturas reprodutivas e, consequentemente, a produtividade da lavoura. "
        "A desfolha é causada pelo consumo do tecido foliar pelas lagartas. Em ataques iniciais, podem aparecer "
        "pequenas raspagens, perfurações e recortes nas folhas. À medida que as larvas crescem, a capacidade de "
        "consumo aumenta e os danos podem se tornar muito mais visíveis. Em infestações severas, grande parte da "
        "superfície foliar pode ser destruída em pouco tempo, limitando a fotossíntese e alterando o equilíbrio "
        "fisiológico da planta. "
        "Na soja, as lagartas desfolhadoras podem atacar desde a fase vegetativa até os estágios reprodutivos. "
        "Durante a floração, a formação de vagens e o enchimento de grãos, uma desfolha intensa tende a ser mais "
        "preocupante porque a demanda por fotoassimilados aumenta. Se muitas folhas forem consumidas nesse período, "
        "a planta pode ter dificuldade para sustentar o potencial produtivo, resultando em vagens menores, menor "
        "massa de grãos e queda de rendimento. "
        "No algodão, o dano foliar também pode reduzir de maneira importante o desempenho das plantas. Além das "
        "folhas, determinadas espécies de lagartas podem atingir estruturas como brotos, botões florais, flores e "
        "maçãs, ampliando o prejuízo. A perda de tecido foliar diminui a capacidade fotossintética e pode interferir "
        "na formação e retenção das estruturas reprodutivas. "
        "O monitoramento frequente da lavoura é essencial para evitar que a população de lagartas alcance níveis "
        "capazes de provocar perdas econômicas significativas. Em soja, métodos de amostragem como o pano de batida "
        "ajudam a estimar a quantidade de insetos presentes. O controle eficiente deve fazer parte de um programa "
        "de Manejo Integrado de Pragas, no qual a decisão de intervir é baseada em monitoramento, nível de dano "
        "econômico e conhecimento da biologia dos insetos. Diversos inimigos naturais contribuem para reduzir as "
        "populações de lagartas, entre eles parasitoides, predadores e microrganismos entomopatogênicos. "
        "Quando o controle químico é necessário, a aplicação deve considerar a espécie-alvo, o estágio das lagartas "
        "e o nível de infestação. O uso repetitivo e inadequado do mesmo mecanismo de ação pode favorecer a seleção "
        "de populações resistentes. As lagartas desfolhadoras representam uma ameaça relevante para a soja e o "
        "algodão porque reduzem a área foliar, afetam a fotossíntese e podem comprometer a produção. A combinação "
        "de controle biológico, práticas culturais e uso racional de inseticidas ajuda a preservar a produtividade "
        "de forma sustentável."
    ),

    "Doc 5": (
        "A disponibilidade de água é um dos fatores que mais influenciam o desenvolvimento das plantas e a "
        "estabilidade da produção agrícola. Em sistemas de cultivo orgânico, nos quais o manejo busca conciliar "
        "produtividade, conservação dos recursos naturais e redução de impactos ambientais, o uso eficiente da "
        "água ganha importância ainda maior. Nesse contexto, a irrigação por gotejamento se destaca por aplicar "
        "água de forma localizada, próxima à região das raízes, em pequenas vazões e com maior controle da "
        "quantidade fornecida. Em comparação com métodos que molham grandes áreas de solo, o gotejamento pode "
        "reduzir perdas por evaporação, escoamento superficial e aplicação em locais desnecessários. "
        "Um sistema de gotejamento é formado por fonte de água, unidade de bombeamento, filtros, tubulações e "
        "emissores chamados gotejadores. Esses emissores liberam água lentamente em pontos determinados ao longo "
        "da linha de plantio, concentrando a umidade na zona explorada pelas raízes. O manejo pode ser realizado "
        "por setores, permitindo irrigar apenas as áreas necessárias e ajustar o tempo de funcionamento de acordo "
        "com a fase de desenvolvimento da cultura, as condições climáticas e as características do solo. "
        "A principal vantagem associada ao gotejamento é a possibilidade de utilizar a água de maneira mais "
        "eficiente. Como a aplicação ocorre perto das raízes, uma proporção maior da água fornecida fica disponível "
        "para a planta. O gotejamento procura diminuir perdas por meio de vazões pequenas e frequentes, ajustadas "
        "à necessidade da cultura. Essa característica é particularmente relevante em regiões com disponibilidade "
        "hídrica limitada ou em períodos de estiagem. "
        "No cultivo orgânico, a irrigação por gotejamento apresenta vantagens que vão além da economia de água. "
        "Como a superfície total do solo não precisa ser molhada a cada irrigação, áreas entre as linhas de cultivo "
        "podem permanecer relativamente mais secas, contribuindo para reduzir a germinação de plantas espontâneas. "
        "A aplicação localizada evita molhar continuamente folhas, flores e frutos, o que pode ser favorável ao "
        "manejo de algumas doenças que se desenvolvem em ambientes muito úmidos. "
        "O gotejamento permite trabalhar com irrigações menores e mais frequentes, evitando grandes oscilações de "
        "umidade. A manutenção de condições mais estáveis na zona radicular pode favorecer o crescimento das raízes "
        "e a absorção de nutrientes. Em sistemas orgânicos, o planejamento da irrigação deve estar integrado ao uso "
        "de composto, biofertilizantes e outras fontes permitidas. O gotejamento pode ser combinado com cobertura "
        "morta, palhada, compostagem e outras práticas que aumentam a proteção do solo e diminuem a evaporação. "
        "Apesar das vantagens, o gotejamento exige cuidados técnicos: os emissores podem sofrer entupimentos, por "
        "isso a filtragem da água e a limpeza periódica das linhas são fundamentais. A irrigação por gotejamento é "
        "uma tecnologia importante para sistemas agrícolas que buscam usar a água de forma racional. Sua aplicação "
        "localizada favorece a redução de desperdícios, permite maior controle da umidade do solo e combina-se bem "
        "com práticas de conservação utilizadas no cultivo orgânico."
    ),

}


# ============================================================
# STOPWORDS EM PORTUGUÊS - lista manual, sem biblioteca externa
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
# ÍNDICE INVERTIDO - implementação manual
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
# CÁLCULOS TF-IDF - implementação manual, sem scikit-learn
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
# SIMILARIDADE DE COSSENO - implementação manual (Bônus)
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
# INTERFACE STREAMLIT - aplicação de página única
# ============================================================

st.set_page_config(
    page_title="AgroSearch",
    layout="wide",
)

st.title("🌱 AgroSearch - Motor de Busca Inteligente")
st.markdown("**Recuperação de Informação e Processamento de Linguagem Natural**")
st.divider()


# ============================================================
# SEÇÃO 1 - BASE DE DOCUMENTOS
# ============================================================
st.subheader("Seção 1 - Base de Documentos")


cols_docs = st.columns(2)
for i, (id_doc, texto) in enumerate(documentos.items()):
    with cols_docs[i % 2]:
        with st.expander(f"{id_doc}", expanded=False):
            st.write(texto)

st.divider()


# ============================================================
# SEÇÃO 2 - CONFIGURAÇÕES DE PRÉ-PROCESSAMENTO
# ============================================================
st.subheader("Seção 2 - Configurações de Pre-processamento")
st.markdown(
    "Altere os checkboxes abaixo para ver o impacto em tempo real no vocabulário, "
    "no índice invertido e nos resultados da busca."
)

col_sw, col_st = st.columns(2)
with col_sw:
    usar_stopwords = st.checkbox(
        "Remover Stopwords",
        value=True,
        help="Remove palavras sem valor semântico: artigos, preposições, conjunções etc.",
    )
with col_st:
    usar_stemming = st.checkbox(
        "Aplicar Stemming",
        value=True,
        help="Reduz palavras à raiz removendo sufixos comuns do português.",
    )

# Processamento dinâmico - recalcula tudo ao mudar um checkbox -
docs_processados = {
    id_doc: preprocessar(texto, usar_stopwords, usar_stemming)
    for id_doc, texto in documentos.items()
}

vocabulario = sorted(set(t for tokens in docs_processados.values() for t in tokens))

st.divider()


# ============================================================
# SEÇÃO 3 - PIPELINE DE PRÉ-PROCESSAMENTO
# ============================================================
st.subheader("Seção 3 - Pipeline de Pre-processamento")
st.info(
    "Cada documento passa pelo pipeline: "
    "**Tokenização → Normalização → Stopwords → Stemming**. "
    "O resultado são os tokens que alimentam o índice invertido e o TF-IDF."
)

tabela_pipeline = [
    {
        "Documento": id_doc,
        "Tokens Processados": " | ".join(tokens) if tokens else "(vazio)",
        "Nº de Tokens": len(tokens),
    }
    for id_doc, tokens in docs_processados.items()
]
st.dataframe(pd.DataFrame(tabela_pipeline), use_container_width=True)

col_m1, col_m2 = st.columns([1, 3])
with col_m1:
    st.metric("Termos no vocabulário", len(vocabulario))
with col_m2:
    with st.expander("Ver lista completa do vocabulário"):
        st.write(", ".join(vocabulario) if vocabulario else "Vocabulário vazio.")

st.divider()


# ============================================================
# SEÇÃO 4 - ÍNDICE INVERTIDO
# ============================================================
st.subheader("Seção 4 - Indice Invertido")
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

    with st.expander("Ver indice invertido em formato JSON"):
        st.json({termo: list(docs) for termo, docs in indice_invertido.items()})
else:
    st.warning("Vocabulário vazio. Ajuste as configurações de pré-processamento.")

st.divider()


# ============================================================
# SEÇÃO 5 - CONSULTA (QUERY)
# ============================================================
st.subheader("Seção 5 - Consulta")
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
            "A query ficou vazia após o pré-processamento. "
            "Tente desativar Stopwords/Stemming ou use termos mais específicos."
        )

    if query_tokens:
        st.divider()

        # ============================================================
        # SEÇÕES 6 E 7 - CÁLCULO MANUAL DE TF-IDF
        # ============================================================
        st.subheader("Seções 6 e 7 - Cálculo Manual de TF-IDF")
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

        with st.expander("Tabela completa: todos os termos x todos os documentos", expanded=True):
            st.dataframe(df_detalhes, use_container_width=True)

        df_relevantes = df_detalhes[df_detalhes["Frequência"] > 0]
        if not df_relevantes.empty:
            with st.expander("Filtrado: apenas linhas com Frequência > 0"):
                st.dataframe(df_relevantes, use_container_width=True)

        st.divider()

        # ============================================================
        # SEÇÃO 8 - RANKING POR TF-IDF
        # ============================================================
        st.subheader("Seção 8 - Ranking por TF-IDF")
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
                f"Documento mais relevante: **{melhor_doc}**  |  "
                f"Score TF-IDF: `{round(melhor_score, 6)}`"
            )

            posicoes = ["1º", "2º", "3º", "4º", "5º"]
            tabela_ranking = [
                {
                    "Posição": posicoes[i] if i < len(posicoes) else f"{i + 1}º",
                    "Documento": id_doc,
                    "Score TF-IDF": round(score, 6),
                }
                for i, (id_doc, score) in enumerate(ranking)
            ]
            st.dataframe(pd.DataFrame(tabela_ranking), use_container_width=True)

        st.divider()

        # ============================================================
        # SEÇÃO 9 - SIMILARIDADE DE COSSENO (BÔNUS)
        # ============================================================
        st.subheader("Seção 9 - Similaridade de Cosseno (Bonus)")
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
            })

        resultados_cosseno.sort(key=lambda x: x["Similaridade Cosseno"], reverse=True)

        max_cos = resultados_cosseno[0]["Similaridade Cosseno"] if resultados_cosseno else 0.0

        if max_cos > 0.0:
            melhor_cos_doc = resultados_cosseno[0]["Documento"]
            st.success(
                f"Documento mais similar (Cosseno): **{melhor_cos_doc}**  |  "
                f"Similaridade: `{resultados_cosseno[0]['Similaridade Cosseno']}`"
            )
        else:
            st.warning("Similaridade de cosseno zero para todos os documentos com esta query.")

        st.dataframe(pd.DataFrame(resultados_cosseno), use_container_width=True)

else:
    st.info("Digite uma consulta no campo acima para ver os resultados do motor de busca.")


st.divider()
