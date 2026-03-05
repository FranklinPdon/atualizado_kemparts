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
        return f"{valor/1_000_000:.2f} MM".replace(".", ",")

    elif valor >= 1_000:
        return f"{valor/1_000:.2f} K".replace(".", ",")

    else:
        return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# =====================================================
# METAS
# =====================================================

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
            Meta Prevista: <b>{formatar_numero(meta)}</b><br>
            Realizado: <b>{formatar_numero(realizado)}</b> ({percentual:.2f}%)
            </div>
            """,
            unsafe_allow_html=True
        )

# =====================================================
# KG
# =====================================================

st.markdown("## Indicadores de Volume (KG)")

kg_total = df_filtrado["Quantidade"].sum()

meta_kg = metas_kg.get(mes_nome,0)

percentual_kg = (kg_total/meta_kg*100) if meta_kg>0 else 0

k1,k2,k3 = st.columns(3)

k1.metric("Meta KG",formatar_numero(meta_kg))
k2.metric("KG Vendidos",formatar_numero(kg_total))
k3.metric("% da Meta KG",f"{percentual_kg:.1f}%")

# =====================================================
# PROJEÇÃO DE FECHAMENTO
# =====================================================

st.markdown("## Projeção de Fechamento do Mês")

hoje = datetime.today()

mapa_numero_mes = {
"Janeiro":1,"Fevereiro":2,"Março":3,"Abril":4,
"Maio":5,"Junho":6,"Julho":7,"Agosto":8,
"Setembro":9,"Outubro":10,"Novembro":11,"Dezembro":12
}

numero_mes = mapa_numero_mes.get(mes_nome,hoje.month)

ano = hoje.year

primeiro_dia = datetime(ano,numero_mes,1)

ultimo_dia = datetime(
ano,
numero_mes,
calendar.monthrange(ano,numero_mes)[1]
)

datas_mes = pd.date_range(primeiro_dia,ultimo_dia)

dias_uteis = datas_mes[datas_mes.weekday<5]

dias_passados = dias_uteis[dias_uteis<=hoje]

dias_restantes = dias_uteis[dias_uteis>hoje]

num_passados=len(dias_passados)
num_restantes=len(dias_restantes)
num_total=len(dias_uteis)

media_diaria=faturamento/num_passados if num_passados>0 else 0

projecao=media_diaria*num_total

# =====================================================
# MENSAGEM DE ALERTA PROJEÇÃO
# =====================================================

if projecao >= meta_valor:
    mensagem = "Mantido o volume atual, a projeção indica: Atingimento da meta ao final do mês."
    st.success(mensagem)

else:
    mensagem = "Mantido o volume atual, a projeção indica: Desvio negativo ao final do mês."
    st.warning(mensagem)

valor_restante=meta_valor-faturamento

necessario_dia=valor_restante/num_restantes if num_restantes>0 else 0

p1,p2,p3,p4 = st.columns(4)

p1.metric("Projeção fechamento",formatar_numero(projecao))
p2.metric("Média diária",formatar_numero(media_diaria))
p3.metric("Necessário por dia",formatar_numero(necessario_dia))
p4.metric("Dias úteis restantes",num_restantes)

# =====================================================
# EXPLICAÇÃO - PROJEÇÃO DE FECHAMENTO
# =====================================================
st.expander(" O que significa Projeção de Fechamento do Mês?").write("""
### Explicação Simples

- **Saldo para a Meta**: Quanto ainda falta faturar para atingir a meta total.  
- **Projeção de Fechamento**: Estimativa de faturamento até o fim do mês, baseada na média diária atual (considerando apenas dias úteis).  
- A projeção pode ser menor ou maior que a meta, dependendo do ritmo de vendas.  
- Por isso, os números podem ser diferentes: um é “faltante” e o outro é “previsto”.
""")



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
text="Total"
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
text="Total",
color_discrete_map={
"1º Lugar":"#FFD700",
"Outros":"#1f77b4"
}
)

fig_vendedores.update_layout(height=450,showlegend=False)

st.plotly_chart(fig_vendedores,use_container_width=True)

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
text="Total"
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