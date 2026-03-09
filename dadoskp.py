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
    page_title="Painel de Acompanhamento de Faturamento Diário",
    layout="wide"
)

# =====================================================
# CAPA
# =====================================================

st.image("CAPA.png", use_container_width=True)

st.title("Painel de Acompanhamento de Faturamento Diário")

# =====================================================
# FUNÇÃO FORMATAÇÃO NUMÉRICA
# =====================================================

def formatar_numero(valor):

    if pd.isna(valor):
        return "0"

    valor = float(valor)

    if valor >= 1_000_000:
        return f"{valor/1_000_000:.3f} MM".replace(".", ",")

    elif valor >= 1_000:
        return f"{valor/1_000:.2f} K".replace(".", ",")

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
    "Março": 3186391.65
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

st.markdown("### Filtros")

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

meses_meta = ["Janeiro","Fevereiro","Março"]

colunas = st.columns(3)

for i, mes_meta in enumerate(meses_meta):

    meta = metas_faturamento.get(mes_meta,0)

    realizado = df_filtrado[df_filtrado["Mes"]==mes_meta]["Total"].sum()

    percentual = (realizado/meta*100) if meta>0 else 0

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=percentual,
        number={'suffix': "%",'font':{'size':28}},
        gauge={
            'axis':{'range':[0,120]},
            'bar':{'color':"#2ca02c" if percentual>=100 else "#ff7f0e"},
            'steps':[
                {'range':[0,60],'color':"#f2f2f2"},
                {'range':[60,90],'color':"#e6e6e6"},
                {'range':[90,120],'color':"#d9d9d9"}
            ]
        }
    ))

    fig.update_layout(height=200,margin=dict(t=20,b=0,l=0,r=0))

    with colunas[i]:

        st.markdown(
            f"<h4 style='text-align:center'>{mes_meta}</h4>",
            unsafe_allow_html=True
        )

        st.plotly_chart(fig, use_container_width=True, key=f"velocimetro_{mes_meta}")

        st.markdown(
            f"""
            <div style="text-align:center;border:1px dashed #ccc;padding:6px;font-size:14px">
            Meta Prevista: <b>{formatar_numero(meta)}</b>
            </div>
            """,
            unsafe_allow_html=True
        )

        # =====================================================
# INDICADORES GERAIS DE META
# =====================================================

st.markdown("## Indicadores de Faturamento")

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
        <div style="{titulo_style}">Meta de Faturamento</div>
        <div style="{numero_style}">{formatar_numero(meta_faturamento)}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="{card_style}">
        <div style="{titulo_style}">Faturamento até o momento</div>
        <div style="{numero_style}">{formatar_numero(faturamento_realizado)}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="{card_style}">
        <div style="{titulo_style}">Falta para atingir a meta</div>
        <div style="{numero_style}">{formatar_numero(valor_restante)}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div style="{card_style}">
        <div style="{titulo_style}">Dias úteis restantes</div>
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
# EVOLUÇÃO FATURAMENTO
# =====================================================

st.markdown("## Evolução de Faturamento Mensal")

evolucao = df.groupby("Mes")["Total"].sum().reset_index()

ordem_meses=[
"Janeiro","Fevereiro","Março","Abril","Maio","Junho",
"Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"
]

evolucao["Mes"]=pd.Categorical(evolucao["Mes"],categories=ordem_meses,ordered=True)

evolucao=evolucao.sort_values("Mes")

fig_linha = px.line(
    evolucao,
    x="Mes",
    y="Total",
    markers=True
)

st.plotly_chart(fig_linha,use_container_width=True)

# =====================================================
# TOP PRODUTOS
# =====================================================

st.markdown("## Produtos com maior performance")

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
# RANKING VENDEDORES
# =====================================================

st.markdown("## Ranking de Vendedores")

ranking_vendedores = (
df_filtrado
.groupby("Vendedor 1")["Total"]
.sum()
.sort_values(ascending=False)
.reset_index()
)

ranking_vendedores["Destaque"]="Outros"
ranking_vendedores.loc[0,"Destaque"]="1º Lugar"

fig_vendedores = px.bar(
ranking_vendedores,
x="Vendedor 1",
y="Total",
color="Destaque",
text=ranking_vendedores["Total"].apply(formatar_numero),
color_discrete_map={
"1º Lugar":"#FFD700",
"Outros":"#1f77b4"
}
)

fig_vendedores.update_layout(height=450,showlegend=False)

st.plotly_chart(fig_vendedores,use_container_width=True)


# =====================================================
# FATURAMENTO DIÁRIO POR VENDEDOR
# =====================================================

st.markdown("## Faturamento Diário por Vendedor")

# Agrupar dados
faturamento_vendedor_dia = (
    df_filtrado
    .groupby(["DT Emissao", "Vendedor 1"])["Total"]
    .sum()
    .reset_index()
)

# Ordenar por data
faturamento_vendedor_dia = faturamento_vendedor_dia.sort_values("DT Emissao")

# Criar coluna dia
faturamento_vendedor_dia["Dia"] = faturamento_vendedor_dia["DT Emissao"].dt.day

# Total por dia
total_dia = (
    faturamento_vendedor_dia
    .groupby("Dia")["Total"]
    .sum()
    .reset_index()
)

# =====================================================
# GRÁFICO
# =====================================================

import plotly.graph_objects as go

fig = go.Figure()

# Barras empilhadas por vendedor
vendedores = faturamento_vendedor_dia["Vendedor 1"].unique()

for vendedor in vendedores:
    df_vend = faturamento_vendedor_dia[faturamento_vendedor_dia["Vendedor 1"] == vendedor]

    fig.add_bar(
        x=df_vend["Dia"],
        y=df_vend["Total"],
        name=vendedor,
        text=df_vend["Total"].apply(formatar_numero),
        textposition="inside"
    )

# Linha do total do dia
fig.add_trace(
    go.Scatter(
        x=total_dia["Dia"],
        y=total_dia["Total"],
        mode="lines+markers+text",
        name="Total do Dia",
        text=total_dia["Total"].apply(formatar_numero),
        textposition="top center",
        line=dict(width=3)
    )
)

fig.update_layout(
    barmode="stack",
    height=500,
    xaxis_title="Dia do mês",
    yaxis_title="Faturamento (R$)",
    legend_title="Vendedor",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

# =====================================================
# TOP CLIENTES
# =====================================================

st.markdown("## Clientes que mais compraram no mês")

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