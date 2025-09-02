# 1° passo: Instalar todas as bibliotecas necessárias para esse projeto
# → pip install streamlit pandas plotly requests

# 2° passo: Importando as bibliotecas
import streamlit as st # simplifica a criação de aplicativos web interativos para ciência de dados
import pandas as pd # ferramenta padrão para manipulação e análise de dados
import plotly.express as px # criação de gráficos interativos e esteticamente agradáveis
import requests # pega informações de API's de sites
import pprint # formata a saída de dados para facilitar a leitura

# 3° passo: Puxando os dados do Banco Central do Brasil (BACEN)
def dados_bacen(codigo, data_inicial="01/09/2015", data_final="22/08/2025"):
    try:
        link_1 = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados?formato=json&dataInicial={data_inicial}&dataFinal={data_final}"
        requisicao = requests.get(link_1) # pega os dados da API
        print("🔗 URL usada:", link_1)  # debug
        requisicao.raise_for_status() # Verifica se a requisição foi bem-sucedida
        print("📡 Status code:", requisicao.status_code)  # debug
        print("📦 Conteúdo bruto:", requisicao.text[:200])  # mostra só os 200 primeiros caracteres
        requisicao = requisicao.json() # transforma em JSON
        tabela = pd.DataFrame(requisicao) # transforma a lista de dicionários em um DataFrame (Tabela)
        tabela['data'] = pd.to_datetime(tabela['data'], dayfirst=True)
        tabela['valor'] = tabela['valor'].astype(float)
        return tabela
    except Exception as e:
        st.error(f"Erro ao obter dados do BACEN: {e}")
        return pd.DataFrame()
    
# 4° passo: Puxando os dados do Instituto Brasileiro de Geografia e Estatística (IBGE)
def dados_ibge(codigo, periodo, variavel): # criando uma função que recebe o código da série do IBGE
    try:
        link_2 = f"https://servicodados.ibge.gov.br/api/v3/agregados/{codigo}/periodos/{periodo}/variaveis/{variavel}?localidades=N1[all]"
        requisicao = requests.get(link_2) # pega os dados da API
        requisicao.raise_for_status()  # Verifica se a requisição foi bem-sucedida
        requisicao = requisicao.json() # transforma em JSON
        dados = requisicao[0]['resultados'][0]['series'][0]['serie'] # transforma a lista de dicionários em um DataFrame (Tabela)
        tabela = pd.DataFrame(dados.items(), columns=['período', 'valor'])
        tabela['período'] = pd.to_datetime(tabela['período'], format="%Y%m")
        tabela['valor'] = tabela['valor'].astype(float)
        return tabela
    except Exception as e:
        st.error(f"Erro ao obter dados do IBGE: {e}")
        return pd.DataFrame()

st.title("📊 Dashboard Macroeconômico do Brasil") # Título grande da página

# Taxa Selic - BACEN (código 432)
selic = dados_bacen(432)
print("SELlC - shape:", selic.shape)
print("SELlC - colunas:", selic.columns)
print(selic.head())
fig_selic = px.line(selic, x="data", y="valor", title="Taxa Selic (%)")
st.plotly_chart(fig_selic) # mostra o gráfico na página do Streamlit

# Câmbio Dólar - BACEN (código 1)
cambio = dados_bacen(1)
fig_cambio = px.line(cambio, x="data", y="valor", title="Dólar/Real (R$)")
st.plotly_chart(fig_cambio)

#IPCA - IBGE (código 1737, período 200001-202507, variável 2265)
ipca = dados_ibge(1737, "200001-202507", 2265)
fig_ipca = px.line(ipca, x="período", y="valor", title="IPCA (%)")
st.plotly_chart(fig_ipca)

# PIB Trimestral - IBGE (código 2072, período 200001-202501, variável 933)
pib = dados_ibge(2072, "200001-202501", 933)
fig_pib = px.bar(pib, x="período", y="valor", title="PIB Trimestral (R$ Milhões)")
st.plotly_chart(fig_pib)

# Taxa de Desemprego - IBGE (código 6381, período 201203-202506, variável 4099)
desemprego = dados_ibge(6381, "201203-202506", 4099)
fig_desemprego = px.line(desemprego, x="período", y="valor", title="Taxa de Desemprego (%)")
st.plotly_chart(fig_desemprego)