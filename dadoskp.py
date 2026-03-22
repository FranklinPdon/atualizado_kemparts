import streamlit as st
import pandas as pd
from datetime import datetime
import calendar
import plotly.express as px

import plotly.graph_objects as go

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

df = df[df["Vendedor 1"] != "KP"]

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

col1,col2,col3,col4 = st.columns(4)

with col1:
    vendedor = st.multiselect(
        "Vendedor",
        options=sorted(df["Vendedor 1"].dropna().unique()),
        placeholder="Selecione"
    )

with col2:
    grupo = st.multiselect(
        "Grupo Produto",
        options=sorted(df["Nome Grupo"].dropna().unique()),
        placeholder="Selecione"
    )

with col3:
    estado = st.multiselect(
        "Estado",
        options=sorted(df["Estado"].dropna().unique()),
        placeholder="Selecione"
    )

with col4:
    mes = st.multiselect(
        "Mês",
        options=sorted(df["Mes"].dropna().unique()),
        placeholder="Selecione"
    )

# =====================================================
# FILTRO BASE
# =====================================================

df_filtrado = df.copy()

if vendedor:
    df_filtrado = df_filtrado[df_filtrado["Vendedor 1"].isin(vendedor)]

if grupo:
    df_filtrado = df_filtrado[df_filtrado["Nome Grupo"].isin(grupo)]

if estado:
    df_filtrado = df_filtrado[df_filtrado["Estado"].isin(estado)]

if mes:
    df_filtrado = df_filtrado[df_filtrado["Mes"].isin(mes)]

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
# VELOCÍMETROS META
# =====================================================

st.markdown("## Atingimento de Meta por Mês")

meses_meta = pd.date_range(start="2026-01-01", end="2026-12-01", freq="MS")

meses_meta = [
    mapa_meses[data.strftime("%B")]
    for data in meses_meta
]

# =========================
# CONTROLE DE MESES VISÍVEIS
# =========================

if "meses_visiveis" not in st.session_state:
    st.session_state.meses_visiveis = 3

# quantidade total
total_meses = len(meses_meta)

# meses que vão aparecer
meses_para_mostrar = meses_meta[:st.session_state.meses_visiveis]

# =========================
# VELOCÍMETROS
# =========================

for i in range(0, len(meses_para_mostrar), 3):
    cols = st.columns(3)

    for j, mes_meta in enumerate(meses_para_mostrar[i:i+3]):

        meta = metas_faturamento.get(mes_meta, 0)
        realizado = df_filtrado[df_filtrado["Mes"] == mes_meta]["Total"].sum()
        percentual = (realizado / meta * 100) if meta > 0 else 0

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=percentual,
            number={'suffix': "%", 'font': {'size': 28}},
            gauge={
    'shape': "angular",
    'axis': {'range': [0, 120]},
    'bar': {'color': "#2ca02c" if percentual >= 100 else "#ff7f0e"},
    'steps': [
        {'range': [0, 60], 'color': "#f2f2f2"},
        {'range': [60, 90], 'color': "#e6e6e6"},
        {'range': [90, 120], 'color': "#d9d9d9"}
    ],
    'threshold': {
        'line': {'color': "red", 'width': 4},
        'thickness': 0.75,
        'value': percentual
    }
}
        ))

        fig.update_layout(height=200, margin=dict(t=20, b=0, l=0, r=0))

        with cols[j]:
            st.markdown(f"<h4 style='text-align:center'>{mes_meta}</h4>", unsafe_allow_html=True)

            st.plotly_chart(
                fig,
                use_container_width=True,
                key=f"velocimetro_{mes_meta}_{i}"
            )

            st.markdown(
                f"""
                <div style="text-align:center;border:1px dashed #ccc;padding:8px;font-size:14px">
                    Meta Prevista: <b>{formatar_numero(meta)}</b><br>
                    Realizado: <b>{formatar_numero(realizado)}</b>
                </div>
                """,
                unsafe_allow_html=True
            )

# =========================
# BOTÃO VER MAIS
# =========================

col1, col2 = st.columns(2)

# botão ver mais
with col1:
    if st.session_state.meses_visiveis < total_meses:
        if st.button("🔽 Ver mais meses"):
            st.session_state.meses_visiveis += 3
            st.rerun()

# botão ver menos
with col2:
    if st.session_state.meses_visiveis > 3:
        if st.button("🔼 Ver menos meses"):
            st.session_state.meses_visiveis -= 3
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
# TOP PRODUTOS
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

fig_produtos.update_layout(height=400)

st.plotly_chart(fig_produtos,use_container_width=True)

# =====================================================
# VOLUME POR PRODUTO
# =====================================================

st.markdown("## Volume por Produto (KG)")

top_produtos_kg = (
    df_filtrado
    .groupby("Descricao")["Quantidade"]
    .sum()
    .sort_values(ascending=False)
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

fig_produtos_kg.update_layout(height=400)

st.plotly_chart(fig_produtos_kg,use_container_width=True)

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
# TOP CLIENTES
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

fig_clientes.update_layout(height=400)

st.plotly_chart(fig_clientes,use_container_width=True)

# =====================================================
# VOLUME POR CLIENTE
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

fig_clientes_kg.update_layout(height=400)

st.plotly_chart(fig_clientes_kg,use_container_width=True)

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