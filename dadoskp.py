import streamlit as st
import pandas as pd
from datetime import datetime
import calendar
import plotly.express as px

import plotly.graph_objects as go

meses_ordem = [
    "Janeiro","Fevereiro","Março","Abril","Maio","Junho",
    "Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"
]

# =====================================================
# CONFIGURAÇÃO DA PÁGINA
# =====================================================

st.set_page_config(
    page_title="Painel Executivo de Faturamento",
    layout="wide"
)

# 🎨 CORES PADRÃO (NOVO)
COR_PRINCIPAL = "#0d6efd"
COR_DESTAQUE = "#198754"
COR_ALERTA = "#dc3545"
COR_FUNDO = "#f8f9fa"

# 🔒 ESCONDER MENU (PROFISSIONAL)
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# =====================================================
# CAPA
# =====================================================

st.image("CAPA.png", use_container_width=True)

st.markdown("""
<h1 style='text-align: center; color: #0d6efd; margin-top:10px;'>
Painel Executivo de Faturamento
</h1>

<p style='text-align: center; font-size:16px; color: gray;'>
Acompanhamento diário de performance comercial
</p>
""", unsafe_allow_html=True)

# =====================================================
# FUNÇÃO FORMATAÇÃO NUMÉRICA
# =====================================================

def formatar_numero(valor):

    if pd.isna(valor):
        return "0"

    valor = float(valor)

    if valor >= 1_000_000:
        valor_mm = int((valor / 1_000_000) * 1000) / 1000
        return f"{valor_mm:,.3f}".replace(",", "X").replace(".", ",").replace("X", ".") + " MM"

    elif valor >= 1_000:
        valor_k = int((valor / 1_000) * 100) / 100
        return f"{valor_k:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") + " K"

    else:
        return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# =====================================================
# METAS
# =====================================================

meta_anual = 43307736.07
meta_kg_anual = 2270595

metas_faturamento = {
    "Janeiro": 2436225.96,
    "Fevereiro": 3193147.61,
    "Março": 3186391.65,
    "Abril": 3609736.02,
    "Maio": 3763284.43,
    "Junho": 4370388.36,
    "Julho": 3916873.28,
    "Agosto": 4187091.15,
    "Setembro": 4276090.17,
    "Outubro": 3651020.57,
    "Novembro": 3903881.23,
    "Dezembro": 2813605.64
}

# =====================================================
# METAS POR VENDEDOR
# =====================================================

metas_vendedores = {

"OD":{
"Janeiro":478646.48,"Fevereiro":841806.88,"Março":789901.26,
"Abril":885792.32,"Maio":954052.52,"Junho":918426.65,
"Julho":846802.13,"Agosto":1005106.28,"Setembro":917165.83,
"Outubro":885742.76,"Novembro":963445.45,"Dezembro":579024.51
},

"JF":{
"Janeiro":458428.74,"Fevereiro":760267.39,"Março":853897.07,
"Abril":772218.21,"Maio":983467.90,"Junho":888066.93,
"Julho":1004884.24,"Agosto":1000867.24,"Setembro":988439.01,
"Outubro":827237.38,"Novembro":1005616.93,"Dezembro":516517.88
},

"DK":{
"Janeiro":939131.49,"Fevereiro":879804.44,"Março":830970.87,
"Abril":876621.17,"Maio":768705.53,"Junho":1042012.70,
"Julho":990172.09,"Agosto":1069446.28,"Setembro":980568.86,
"Outubro":975097.08,"Novembro":876107.98,"Dezembro":922547.74
},

"GP":{
"Janeiro":141688.30,"Fevereiro":116539.16,"Março":227075.93,
"Abril":143722.16,"Maio":147879.59,"Junho":193632.74,
"Julho":162163.57,"Agosto":132265.86,"Setembro":224101.73,
"Outubro":116539.16,"Novembro":199606.49,"Dezembro":146927.70
},

"LT":{
"Janeiro":418330.95,"Fevereiro":594729.74,"Março":484546.52,
"Abril":931382.16,"Maio":909178.89,"Junho":1328249.34,
"Julho":912851.25,"Agosto":979405.49,"Setembro":1165814.74,
"Outubro":846404.19,"Novembro":859104.38,"Dezembro":648587.81
}

}

# =====================================================
# METAS KG POR VENDEDOR
# =====================================================

metas_kg_vendedores = {

"OD":{
"Janeiro":23995,"Fevereiro":41415,"Março":40765,
"Abril":44220,"Maio":49110,"Junho":45580,
"Julho":43760,"Agosto":50740,"Setembro":47260,
"Outubro":44470,"Novembro":49550,"Dezembro":28960
},

"JF":{
"Janeiro":20370,"Fevereiro":33235,"Março":37010,
"Abril":34665,"Maio":39450,"Junho":40425,
"Julho":44160,"Agosto":43150,"Setembro":43230,
"Outubro":36280,"Novembro":41560,"Dezembro":22880
},

"DK":{
"Janeiro":58345,"Fevereiro":57965,"Março":54235,
"Abril":61095,"Maio":49365,"Junho":68135,
"Julho":62700,"Agosto":69037,"Setembro":61030,
"Outubro":65165,"Novembro":55805,"Dezembro":62505
},

"GP":{
"Janeiro":9675,"Fevereiro":9045,"Março":14891,
"Abril":10095,"Maio":9995,"Junho":13795,
"Julho":11095,"Agosto":10291,"Setembro":14695,
"Outubro":9045,"Novembro":12645,"Dezembro":11291
},

"LT":{
"Janeiro":14285,"Fevereiro":22770,"Março":20470,
"Abril":41120,"Maio":42920,"Junho":62800,
"Julho":41130,"Agosto":43290,"Setembro":60260,
"Outubro":39850,"Novembro":41810,"Dezembro":31710
}

}

metas_kg = {
    "Janeiro": 126670,
    "Fevereiro": 164430,
    "Março": 167371,
    "Abril": 191195,
    "Maio": 190840,
    "Junho": 230735,
    "Julho": 202845,
    "Agosto": 216508,
    "Setembro": 226475,
    "Outubro": 194810,
    "Novembro": 201370,
    "Dezembro": 157346
}

# =====================================================
# CARREGAR PLANILHA
# =====================================================

fsp = pd.read_excel("BASE_KEMPARTS.xlsx", sheet_name="FSP")
fsc = pd.read_excel("BASE_KEMPARTS.xlsx", sheet_name="FSC")

df = pd.concat([fsp, fsc])

#  PADRONIZA NOME DOS CLIENTES (EVITA ERRO NO RANKING)
df["Nome"] = df["Nome"].astype(str).str.strip().str.upper()

df["Natureza"] = df["Natureza"].str.strip()
df["Descricao"] = df["Descricao"].str.strip()
df["Vendedor 1"] = df["Vendedor 1"].str.strip()


# =====================================================
# FILTRAGEM BLINDADA (PARA BATER OS 4.872 MM)
# =====================================================

# 1. Limpeza profunda: remove espaços duplos e caracteres estranhos
def limpar_texto(txt):
    txt = str(txt).upper().strip()
    return " ".join(txt.split()) # Remove espaços duplos no meio da frase

df["Natureza"] = df["Natureza"].apply(limpar_texto)
df["Descricao"] = df["Descricao"].apply(limpar_texto)
df["Vendedor 1"] = df["Vendedor 1"].apply(limpar_texto)

# 2. Lista de Termos Proibidos (Filtro por palavra-chave parcial)
# Se a natureza CONTIVER qualquer um desses termos, ela será excluída.
termos_proibidos = [
    "AMOSTRA GRATIS",
    "DEPOSITO FECHADO",
    "CONTA E ORDEM TERC", # Pega a linha dos 95k mesmo com erro de caractere
    "NAO ESPECIFICADO",    # Pega "OUTRA SAIDA... NAO ESPECIFICADO"
    "COMODATO",
    "CONSERTO",
    "BONIFICACAO",
    "BRINDE"
]

# Aplicamos a exclusão por termo parcial (Muito mais seguro para o Protheus)
for termo in termos_proibidos:
    df = df[~df["Natureza"].str.contains(termo, na=False)]

# 3. Regras Específicas
df = df[df["Descricao"] != "COMPLEMENTO DE ICMS"]

# Regra do Vendedor KP (Mantém apenas Exportação)
# Usamos 'contains' aqui também para garantir que pegue a Exportação
N_EXP = "EXPORTACAO" 

df = df[
    (df["Vendedor 1"] != "KP") | 
    ((df["Vendedor 1"] == "KP") & (df["Natureza"].str.contains(N_EXP, na=False)))
]

df["DT Emissao"] = pd.to_datetime(df["DT Emissao"])

df["Mes"] = df["DT Emissao"].dt.month_name()

mapa_meses = {
    "January":"Janeiro",
    "February":"Fevereiro",
    "March":"Março",
    "April":"Abril",
    "May":"Maio",
    "June":"Junho",
    "July":"Julho",
    "August":"Agosto",
    "September":"Setembro",
    "October":"Outubro",
    "November":"Novembro",
    "December":"Dezembro"
}

df["Mes"] = df["Mes"].map(mapa_meses)


# =====================================================
# FILTROS
# =====================================================

st.divider()

st.markdown("""
##  Filtros Inteligentes
Selecione os parâmetros para análise dos dados
""")

# Criamos 5 colunas: a primeira é mais larga para caber o calendário
col_data, col1, col2, col3, col4 = st.columns([2, 1, 1, 1, 1])

with col_data:
    # Definindo as datas mínima e máxima que existem na sua planilha
    data_min = df["DT Emissao"].min().date()
    data_max = df["DT Emissao"].max().date()
    
    # Este é o campo onde você clica e seleciona o período (Início e Fim)
    periodo = st.date_input(
        "Período de Emissão (Início e Fim)",
        value=(data_min, data_max),
        min_value=data_min,
        max_value=data_max,
        format="DD/MM/YYYY"
    )

with col1:
    mes = st.multiselect(
        "Mês",
        options=meses_ordem,
        placeholder="Selecione"
    )

with col2:
    vendedor = st.multiselect(
        "Vendedor",
        options=sorted(df["Vendedor 1"].dropna().unique()),
        placeholder="Selecione"
    )

with col3:
    grupo = st.multiselect(
        "Grupo Produto",
        options=sorted(df["Nome Grupo"].dropna().unique()),
        placeholder="Selecione"
    )

with col4:
    estado = st.multiselect(
        "Estado",
        options=sorted(df["Estado"].dropna().unique()),
        placeholder="Selecione"
    )



# (Mantenha o restante dos seus filtros de vendedor, grupo, etc., abaixo daqui)

# =====================================================
# FILTRO BASE (ESSA PARTE CONECTA O FILTRO AOS DADOS)
# =====================================================

df_filtrado = df.copy()

# filtro de data
if isinstance(periodo, tuple) and len(periodo) == 2:
    data_inicio, data_fim = periodo
    df_filtrado = df_filtrado[
        (df_filtrado["DT Emissao"].dt.date >= data_inicio) &
        (df_filtrado["DT Emissao"].dt.date <= data_fim)
    ]

# filtros adicionais
if vendedor:
    df_filtrado = df_filtrado[df_filtrado["Vendedor 1"].isin(vendedor)]
if grupo:
    df_filtrado = df_filtrado[df_filtrado["Nome Grupo"].isin(grupo)]
if estado:
    df_filtrado = df_filtrado[df_filtrado["Estado"].isin(estado)]
if mes:
    df_filtrado = df_filtrado[df_filtrado["Mes"].isin(mes)]

# 👇 FORA do if mes (IMPORTANTE)
if mes and len(mes) == 1:
    mes_nome = mes[0]
else:
    mes_nome = None
# =====================================================
# FATURAMENTO
# =====================================================

faturamento = df_filtrado["Total"].sum()

if mes:
    mes_nome = mes[0]
else:
    mes_nome = datetime.today().strftime("%B")
    mes_nome = mapa_meses.get(mes_nome, mes_nome)

meta_valor = metas_faturamento.get(mes_nome,0)


# =====================================================
# INDICADORES DE PROGRESSO CIRCULAR - DINÂMICO
# =====================================================

st.markdown("## Atingimento de Meta por Mês")

def criar_progresso_circular(meta, realizado, nome_mes):
    percentual = (realizado / meta * 100) if meta > 0 else 0
    progresso_visual = min(percentual, 100)
    restante_visual = 100 - progresso_visual

    fig = go.Figure()

    fig.add_trace(go.Pie(
        values=[progresso_visual, restante_visual],
        hole=0.75,
        marker=dict(colors=['#bc16a4', '#e0e0e0']), 
        sort=False,
        direction='clockwise',
        showlegend=False,
        hoverinfo='skip',
        textinfo='none'
    ))

    # Número grande e centralizado (cor adaptativa ao fundo)
    fig.add_annotation(
        text=f"<b style='font-size:35px;'>{percentual:.0f}%</b>",
        x=0.5, y=0.5, showarrow=False
    )

    fig.update_layout(
        height=250, # Aumentado para melhor visualização
        margin=dict(t=10, b=10, l=0, r=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    return fig

@st.dialog("Resumo Mensal Detalhado")
def exibir_resumo_detalhado(mes_nome, df_mes, meta_valor):
    # 1. Cálculos de Faturamento e Meta
    faturado = df_mes["Total"].sum()
    perc = (faturado / meta_valor * 100) if meta_valor > 0 else 0
    provisao = max(meta_valor - faturado, 0)
    
    # 2. Identificação dos Destaques
    if not df_mes.empty:
        # Vendedor e Cliente (por Valor)
        vendedor_top = df_mes.groupby("Vendedor 1")["Total"].sum().idxmax()
        cliente_top = df_mes.groupby("Nome")["Total"].sum().idxmax() # NOVO: Cliente que mais comprou
        
        # Produto por Valor
        produto_top_valor = df_mes.groupby("Descricao")["Total"].sum().idxmax()
        
        # Produto por Volume (KG)
        top_produto_kg_nome = df_mes.groupby("Descricao")["Quantidade"].sum().idxmax()
        top_produto_kg_valor = df_mes.groupby("Descricao")["Quantidade"].sum().max()
        texto_produto_kg = f"{top_produto_kg_nome} ({formatar_numero(top_produto_kg_valor)} KG)"
        
        estado_top = df_mes.groupby("Estado")["Total"].sum().idxmax()
    else:
        vendedor_top = cliente_top = produto_top_valor = texto_produto_kg = estado_top = "-"

    # 3. Interface Visual do Popup
    st.markdown(f"### 📅 Relatório de {mes_nome}")
    
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Meta Planejada", formatar_numero(meta_valor))
        st.metric("Faturado Real", formatar_numero(faturado))
    with c2:
        st.metric("Atingimento", f"{perc:.1f}%")
        st.metric("Provisão para a Meta", formatar_numero(provisao))

    st.divider()
    st.markdown("**🏆 Destaques do Mês:**")
    
    st.info(f"👤 **Vendedor destaque:** {vendedor_top}")
    st.info(f"🏢 **Cliente destaque:** {cliente_top}") # EXIBIÇÃO DO CLIENTE
    st.success(f"💰 **Produto destaque (Valor):** {produto_top_valor}")
    st.success(f"⚖️ **Produto destaque (Volume):** {texto_produto_kg}")
    st.warning(f"📍 **Estado que mais comprou:** {estado_top}")
    
    if st.button("Fechar", use_container_width=True):
        st.rerun()

def exibir_meses_grid(lista_meses):
    num_cols = min(len(lista_meses), 6) if len(lista_meses) > 0 else 1
    cols = st.columns(num_cols)
    
    for i, m in enumerate(lista_meses):
        meta_m = metas_faturamento.get(m, 0)
        # Filtramos os dados específicos deste mês para o resumo do Popup
        df_mes = df_filtrado[df_filtrado["Mes"] == m]
        realizado_m = df_mes["Total"].sum()
        
        with cols[i % num_cols]:
            st.markdown(f"<h3 style='text-align:center;'>{m}</h3>", unsafe_allow_html=True)
            st.plotly_chart(criar_progresso_circular(meta_m, realizado_m, m), use_container_width=True, key=f"circ_{m}")
            
            # 1. Botão do Popup
            if st.button(f"Ver Detalhes {m}", key=f"btn_resumo_{m}", use_container_width=True):
                exibir_resumo_detalhado(m, df_mes, meta_m)

            # 2. Exibição da Meta e Realizado abaixo do botão
            st.markdown(
                f"""
                <div style="text-align:center; line-height:1.4; margin-top:10px; margin-bottom:30px;">
                    <span style="font-size:14px; opacity:0.8;">Meta</span><br>
                    <b style="font-size:18px;">{formatar_numero(meta_m)}</b><br>
                    <span style="font-size:14px; opacity:0.8; margin-top:8px; display:inline-block;">Realizado</span><br>
                    <b style="font-size:18px;">{formatar_numero(realizado_m)}</b>
                </div>
                """, unsafe_allow_html=True
            )
# --- LÓGICA DE EXIBIÇÃO ---

# Variável 'mes' vem do seu multiselect lá em cima
if mes:
    # Se o usuário selecionou meses no filtro, mostra APENAS eles
    exibir_meses_grid(mes)
else:
    # Caso contrário, mostra o comportamento padrão por semestres
    if "mostrar_2_semestre" not in st.session_state:
        st.session_state.mostrar_2_semestre = False

    st.markdown("### 1º Semestre")
    exibir_meses_grid(meses_ordem[0:6])

    if not st.session_state.mostrar_2_semestre:
        if st.button("Visualizar 2º Semestre"):
            st.session_state.mostrar_2_semestre = True
            st.rerun()
    else:
        st.markdown("### 2º Semestre")
        exibir_meses_grid(meses_ordem[6:12])
        
        if st.button("Ocultar 2º Semestre"):
            st.session_state.mostrar_2_semestre = False
            st.rerun()

# =====================================================
# INDICADORES GERAIS DE META
# =====================================================

st.divider()

st.markdown("""
##  Indicadores Executivos
Visão geral do desempenho de faturamento
""")

# faturamento realizado
faturamento_realizado = df_filtrado["Total"].sum()

# meta anual
meta_total = meta_anual

# se tiver filtro de mês usa meta do mês
if mes:
    meta_faturamento = metas_faturamento.get(mes_nome,0)
else:
    meta_faturamento = meta_total

# valor restante para meta
valor_restante = max(meta_faturamento - faturamento_realizado,0)

# =============================
# CÁLCULO DIAS ÚTEIS
# =============================

ano = 2026

def calcular_dias_uteis(inicio,fim):
    datas = pd.date_range(inicio,fim)
    return sum(1 for d in datas if d.weekday() < 5)

hoje = datetime.today().date()

# se filtrar mês
if mes:

    mapa_numero_mes = {
        "Janeiro":1,"Fevereiro":2,"Março":3,"Abril":4,
        "Maio":5,"Junho":6,"Julho":7,"Agosto":8,
        "Setembro":9,"Outubro":10,"Novembro":11,"Dezembro":12
    }

    numero_mes = mapa_numero_mes.get(mes_nome,hoje.month)

    inicio = datetime(ano,numero_mes,1)
    fim = datetime(ano,numero_mes,calendar.monthrange(ano,numero_mes)[1])

    dias_uteis_restantes = calcular_dias_uteis(hoje,fim)

else:

    inicio = pd.to_datetime(hoje)
    fim = datetime(ano,12,31)

    dias_uteis_restantes = calcular_dias_uteis(inicio,fim)

# =============================
# KPIs VISUAIS
# =============================

col1, col2, col3, col4 = st.columns(4)

card_style = """
background: linear-gradient(135deg, #0d6efd, #0a58ca);
padding:22px;
border-radius:12px;
text-align:center;
box-shadow:0 6px 16px rgba(0,0,0,0.25);
transition: all 0.3s ease;
"""

titulo_style = """
font-size:13px;
color:#e9ecef;
margin-bottom:6px;
font-weight:500;
letter-spacing:0.5px;
"""

numero_style = """
font-size:28px;
color:white;
font-weight:bold;
margin:0;
"""

with col1:
    st.markdown(f"""
    <div style="{card_style}">
        <div style="{titulo_style}">Meta de Faturamento</div>
        <div style="{numero_style}">{formatar_numero(meta_faturamento)}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="{card_style}">
        <div style="{titulo_style}">Faturado</div>
        <div style="{numero_style}">{formatar_numero(faturamento_realizado)}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="{card_style}">
        <div style="{titulo_style}">Provisão Faturamento</div>
        <div style="{numero_style}">{formatar_numero(valor_restante)}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div style="{card_style}">
        <div style="{titulo_style}">Dias a Faturar</div>
        <div style="{numero_style}">{dias_uteis_restantes}</div>
    </div>
    """, unsafe_allow_html=True)   

# =====================================================
# FATURAMENTO DIÁRIO
# =====================================================

st.markdown("## Faturamento Diário")

# agrupar faturamento por dia
faturamento_dia = (
    df_filtrado
    .groupby("DT Emissao")["Total"]
    .sum()
    .reset_index()
)

# ordenar por data
faturamento_dia = faturamento_dia.sort_values("DT Emissao")

# criar coluna para gráfico
faturamento_dia["Data"] = faturamento_dia["DT Emissao"].dt.strftime("%b %d")

# calcular média diária
media_diaria = faturamento_dia["Total"].mean()

# identificar melhor dia
melhor_dia = faturamento_dia["Total"].max()

# cor das barras
cores = [
    "#FFD700" if valor == melhor_dia else "#1f77b4"
    for valor in faturamento_dia["Total"]
]

# gráfico
fig_faturamento = go.Figure()

# barras
fig_faturamento.add_trace(
    go.Bar(
        x=faturamento_dia["Data"],
        y=faturamento_dia["Total"],
        marker_color=cores,
        name="Faturamento Diário",
        text=faturamento_dia["Total"].apply(formatar_numero),
        textposition="outside"
    )
)

# linha média
fig_faturamento.add_trace(
    go.Scatter(
        x=faturamento_dia["Data"],
        y=[media_diaria]*len(faturamento_dia),
        mode="lines",
        name="Média diária",
        line=dict(dash="dash")
    )
)

fig_faturamento.update_layout(
    height=400,
    yaxis_title="Faturamento (R$)",
    xaxis_title="Dia do mês",
    showlegend=True
)

st.plotly_chart(fig_faturamento, use_container_width=True)        

# =====================================================
# INDICADORES ESPECÍFICOS DE EXPORTAÇÃO
# =====================================================

st.divider()
st.markdown("## Exportação")

# Filtramos apenas as linhas que são de exportação na base filtrada
NATUREZA_EXPORTACAO = "EXPORTACAO DE MERCADORIAS RECEB. FIM ESPEC. EXPORTACAO"
df_exportacao = df_filtrado[df_filtrado["Natureza"] == NATUREZA_EXPORTACAO]

# Inicializa o estado do botão de exportação se não existir
if "mostrar_2_semestre_export" not in st.session_state:
    st.session_state.mostrar_2_semestre_export = False

def exibir_exportacao_grid(lista_meses):
    cols = st.columns(6)
    for i, m in enumerate(lista_meses):
        faturado_export = df_exportacao[df_exportacao["Mes"] == m]["Total"].sum()
        
        with cols[i]:
            st.markdown(f"<p style='text-align:center; font-weight:bold; color:#0d6efd; margin-bottom:5px; font-size:16px;'>{m}</p>", unsafe_allow_html=True)
            
            # Card estilizado com Números Maiores (24px)
            st.markdown(
                f"""
                <div style="background:rgba(13, 110, 253, 0.05); padding:15px; border-radius:10px; text-align:center; border: 1px solid rgba(13, 110, 253, 0.3); min-height:100px; display: flex; flex-direction: column; justify-content: center;">
                    <span style="font-size:13px; opacity:0.7;">Faturado Exportação</span><br>
                    <b style="font-size:24px; color:#bc16a4; display:block; margin-top:5px;">{formatar_numero(faturado_export)}</b>
                </div>
                """, unsafe_allow_html=True
            )

# --- LÓGICA DE EXIBIÇÃO EXPORTAÇÃO ---

if mes:
    # Se houver filtro de mês no topo, mostra apenas os selecionados
    exibir_exportacao_grid(mes)
else:
    # 1º Semestre Exportação
    st.markdown("### 1º Semestre - Exportação")
    exibir_exportacao_grid(meses_ordem[0:6])

    # Botão para o 2º Semestre de Exportação
    if not st.session_state.mostrar_2_semestre_export:
        if st.button("Visualizar 2º Semestre Exportação", key="btn_exp_v"):
            st.session_state.mostrar_2_semestre_export = True
            st.rerun()
    else:
        # 2º Semestre Exportação
        st.markdown("### 2º Semestre - Exportação")
        exibir_exportacao_grid(meses_ordem[6:12])
        
        if st.button("Ocultar 2º Semestre Exportação", key="btn_exp_o"):
            st.session_state.mostrar_2_semestre_export = False
            st.rerun()


# =====================================================
# KG
# =====================================================

st.markdown("## Indicadores de Volume (KG)")

kg_total = df_filtrado["Quantidade"].sum()

# definir meta correta
if mes:
    meta_kg = metas_kg.get(mes_nome,0)
else:
    meta_kg = meta_kg_anual

percentual_kg = (kg_total/meta_kg*100) if meta_kg>0 else 0

col1, col2, col3 = st.columns(3)

card_style = """
background:#0d6efd;
padding:22px;
border-radius:10px;
text-align:center;
box-shadow:0 2px 8px rgba(0,0,0,0.15);
"""

titulo_style = """
font-size:14px;
color:#cfe2ff;
margin-bottom:6px;
font-weight:500;
"""

numero_style = """
font-size:26px;
color:white;
font-weight:600;
margin:0;
"""

with col1:
    st.markdown(f"""
    <div style="{card_style}">
        <div style="{titulo_style}">Meta KG</div>
        <div style="{numero_style}">{formatar_numero(meta_kg)}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="{card_style}">
        <div style="{titulo_style}">KG Vendidos</div>
        <div style="{numero_style}">{formatar_numero(kg_total)}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="{card_style}">
        <div style="{titulo_style}">% da Meta KG</div>
        <div style="{numero_style}">{percentual_kg:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)



# =====================================================
# EVOLUÇÃO FATURAMENTO (ORÇADO VS REALIZADO)
# =====================================================

st.markdown("## Evolução de Faturamento Mensal")

realizado = (
    df
    .groupby("Mes")["Total"]
    .sum()
    .reset_index()
)

realizado["Orçado"] = realizado["Mes"].map(metas_faturamento)

ordem_meses = [
"Janeiro","Fevereiro","Março","Abril","Maio","Junho",
"Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"
]

realizado["Mes"] = pd.Categorical(
    realizado["Mes"],
    categories=ordem_meses,
    ordered=True
)

realizado = realizado.sort_values("Mes")

fig = go.Figure()

fig.add_bar(
    x=realizado["Mes"],
    y=realizado["Total"],
    name="Realizado",
    text=realizado["Total"].apply(formatar_numero),
    textposition="outside"
)

fig.add_bar(
    x=realizado["Mes"],
    y=realizado["Orçado"],
    name="Orçado",
    text=realizado["Orçado"].apply(formatar_numero),
    textposition="outside"
)

fig.update_layout(
    barmode="group",
    height=450,
    yaxis_title="Faturamento (R$)"
)

st.plotly_chart(fig,use_container_width=True)

# =====================================================
# TOP PRODUTOS (MAIOR NO TOPO)
# =====================================================

st.markdown("## Faturamento por Produto")

top_produtos = (
    df_filtrado
    .groupby("Descricao")["Total"]
    .sum()
    .sort_values(ascending=False)
    .head(9)
    .reset_index()
)

fig_produtos = px.bar(
    top_produtos,
    x="Total",
    y="Descricao",
    orientation="h",
    text=top_produtos["Total"].apply(formatar_numero)
)

# INVERTE O EIXO PARA O MAIOR FICAR EM CIMA
fig_produtos.update_yaxes(autorange="reversed")

fig_produtos.update_layout(height=400)

st.plotly_chart(fig_produtos, use_container_width=True)


# =====================================================
# VOLUME POR PRODUTO (KG) - ORDENADO (MAIOR NO TOPO)
# =====================================================

st.markdown("## Volume por Produto (KG)")

top_produtos_kg = (
    df_filtrado
    .groupby("Descricao")["Quantidade"]
    .sum()
    .sort_values(ascending=False) # Mantemos a ordenação do maior para o menor
    .head(9)
    .reset_index()
)

fig_produtos_kg = px.bar(
    top_produtos_kg,
    x="Quantidade",
    y="Descricao",
    orientation="h",
    text=top_produtos_kg["Quantidade"].apply(formatar_numero)
)

# ESTA É A LINHA QUE VOCÊ PRECISA ADICIONAR:
fig_produtos_kg.update_yaxes(autorange="reversed")

fig_produtos_kg.update_layout(height=400)

st.plotly_chart(fig_produtos_kg, use_container_width=True)

# =====================================================
# RANKING VENDEDORES (REALIZADO VS META)
# =====================================================

st.markdown("## Ranking de Vendedores")

ranking_vendedores = (
    df_filtrado
    .groupby("Vendedor 1")["Total"]
    .sum()
    .reset_index()
)

metas_lista = []

for vendedor in ranking_vendedores["Vendedor 1"]:

    if vendedor in metas_vendedores:

        if mes:
            meta_vendedor = metas_vendedores[vendedor].get(mes_nome,0)
        else:
            meta_vendedor = sum(metas_vendedores[vendedor].values())

    else:
        meta_vendedor = 0

    metas_lista.append(meta_vendedor)

ranking_vendedores["Meta"] = metas_lista

ranking_vendedores = ranking_vendedores.sort_values("Total",ascending=False)

fig_vendedores = go.Figure()

# realizado
fig_vendedores.add_bar(
    x=ranking_vendedores["Vendedor 1"],
    y=ranking_vendedores["Total"],
    name="Realizado",
    text=ranking_vendedores["Total"].apply(formatar_numero),
    textposition="outside"
)

# meta
fig_vendedores.add_bar(
    x=ranking_vendedores["Vendedor 1"],
    y=ranking_vendedores["Meta"],
    name="Meta",
    text=ranking_vendedores["Meta"].apply(formatar_numero),
    textposition="outside"
)

fig_vendedores.update_layout(
    barmode="group",
    height=450,
    yaxis_title="Faturamento (R$)"
)

st.plotly_chart(fig_vendedores,use_container_width=True)

# =====================================================
# VOLUME POR VENDEDOR (KG VS META)
# =====================================================

st.markdown("## Volume por Vendedor (KG)")

volume_vendedores = (
    df_filtrado
    .groupby("Vendedor 1")["Quantidade"]
    .sum()
    .reset_index()
)

metas_lista = []

for vendedor in volume_vendedores["Vendedor 1"]:

    if vendedor in metas_kg_vendedores:

        if mes:
            meta_vendedor = metas_kg_vendedores[vendedor].get(mes_nome,0)
        else:
            meta_vendedor = sum(metas_kg_vendedores[vendedor].values())

    else:
        meta_vendedor = 0

    metas_lista.append(meta_vendedor)

volume_vendedores["Meta KG"] = metas_lista

volume_vendedores = volume_vendedores.sort_values("Quantidade",ascending=False)

fig_volume = go.Figure()

fig_volume.add_bar(
    x=volume_vendedores["Vendedor 1"],
    y=volume_vendedores["Quantidade"],
    name="KG Vendido",
    text=volume_vendedores["Quantidade"].apply(formatar_numero),
    textposition="outside"
)

fig_volume.add_bar(
    x=volume_vendedores["Vendedor 1"],
    y=volume_vendedores["Meta KG"],
    name="Meta KG",
    text=volume_vendedores["Meta KG"].apply(formatar_numero),
    textposition="outside"
)

fig_volume.update_layout(
    barmode="group",
    height=450,
    yaxis_title="Volume (KG)"
)

st.plotly_chart(fig_volume,use_container_width=True)


# =====================================================
# PRINCIPAIS CLIENTES (MAIOR NO TOPO)
# =====================================================

st.markdown("## Principais Clientes")

ranking_clientes = (
    df_filtrado
    .groupby("Nome")["Total"]
    .sum()
    .sort_values(ascending=False)
    .head(9)
    .reset_index()
)

fig_clientes = px.bar(
    ranking_clientes,
    x="Total",
    y="Nome",
    orientation="h",
    text=ranking_clientes["Total"].apply(formatar_numero)
)

# INVERTE O EIXO PARA O MAIOR FICAR NO TOPO
fig_clientes.update_yaxes(autorange="reversed")

fig_clientes.update_layout(height=400)

st.plotly_chart(fig_clientes, use_container_width=True)

# =====================================================
# VOLUME POR CLIENTE (KG) - MAIOR NO TOPO
# =====================================================

st.markdown("## Volume por Cliente (KG)")

clientes_kg = (
    df_filtrado
    .groupby("Nome")["Quantidade"]
    .sum()
    .sort_values(ascending=False)
    .head(9)
    .reset_index()
)

fig_clientes_kg = px.bar(
    clientes_kg,
    x="Quantidade",
    y="Nome",
    orientation="h",
    text=clientes_kg["Quantidade"].apply(formatar_numero)
)

# INVERTE O EIXO PARA O MAIOR FICAR NO TOPO
fig_clientes_kg.update_yaxes(autorange="reversed")

fig_clientes_kg.update_layout(height=400)

st.plotly_chart(fig_clientes_kg, use_container_width=True)

# =====================================================
# FATURAMENTO POR ESTADO
# =====================================================

st.markdown("## Participação de Faturamento por Estado")

faturamento_estado = (
df_filtrado
.groupby("Estado")["Total"]
.sum()
.sort_values(ascending=False)
.reset_index()
)

fig_estado = px.pie(
faturamento_estado,
names="Estado",
values="Total",
hole=0.4
)

fig_estado.update_traces(
textposition="inside",
textinfo="percent+label+value"
)

st.plotly_chart(fig_estado,use_container_width=True)