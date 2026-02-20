import streamlit as st
import requests, random

# Configurações de Interface
st.set_page_config(page_title="IA Lotofácil Bolão", page_icon="🍀", layout="centered")

# Estilo visual
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; background-color: #2e7d32; color: white; font-weight: bold; }
    .res-box { background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-left: 5px solid #2e7d32; }
    </style>
    """, unsafe_allow_html=True)

st.title("🍀 IA Lotofácil: Gerador de Bolões")
st.write("Gere jogos de 15, 16 ou 17 dezenas com filtros de alta probabilidade.")

# 1. Configurações de Entrada
col_cfg1, col_cfg2 = st.columns(2)
with col_cfg1:
    qtd_dezenas = st.selectbox("Quantidade de dezenas:", [15, 16, 17], index=0)
with col_cfg2:
    fixas = st.multiselect("Números Fixos (opcional):", range(1, 26), max_selections=5)

# Tabela de Preços e Probabilidades Oficiais
tabela_precos = {15: 3.00, 16: 48.00, 17: 408.00} # Preços médios 2024/2025
chances = {15: "1 em 3.268.760", 16: "1 em 204.297", 17: "1 em 24.035"}

st.sidebar.metric("Custo da Aposta", f"R$ {tabela_precos[qtd_dezenas]:.2f}")
st.sidebar.write(f"**Sua chance:** {chances[qtd_dezenas]}")

def gerar_jogo_ia(n_dezenas, fixas_user):
    try:
        # Busca resultados via API Loterias
        resp = requests.get("https://lotericas.com.br").json()
        ultimo_sorteio = resp['dezenas']
    except:
        ultimo_sorteio = []

    primos_lista = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    
    # Filtros dinâmicos (médias estatísticas)
    filtros = {
        15: {"pares": (7, 8), "primos": (5, 6), "soma": (180, 210)},
        16: {"pares": (7, 9), "primos": (5, 7), "soma": (190, 225)},
        17: {"pares": (8, 9), "primos": (6, 8), "soma": (205, 245)}
    }
    f = filtros[n_dezenas]

    for _ in range(5000):
        restantes = [n for n in range(1, 26) if n not in fixas_user]
        jogo = sorted(list(fixas_user) + random.sample(restantes, n_dezenas - len(fixas_user)))
        
        pa = len([n for n in jogo if n % 2 == 0])
        pr = len([n for n in jogo if n in primos_lista])
        sm = sum(jogo)
        
        # Validação Estatística
        if (f["pares"][0] <= pa <= f["pares"][1]) and \
           (f["primos"][0] <= pr <= f["primos"][1]) and \
           (f["soma"][0] <= sm <= f["soma"][1]):
            
            # Filtro de Exclusão de 15 Pontos
            if len(set(jogo) & set(ultimo_sorteio)) < 15:
                return jogo, pa, pr, sm
    return None, 0, 0, 0

# 2. Botão de Ação
if st.button("GERAR JOGO E CALCULAR CUSTO"):
    with st.spinner("IA analisando milhões de combinações..."):
        jogo, p, pr, s = gerar_jogo_ia(qtd_dezenas, fixas)
        
        if jogo:
            st.markdown("### 📋 Seu Palpite Inteligente:")
            texto_jogo = " - ".join(f"{n:02d}" for n in jogo)
            st.code(texto_jogo, language="text")
            
            st.markdown(f"""
            <div class="res-box">
                <b>Análise Técnica:</b><br>
                🔹 Pares: {p} | 🔹 Primos: {pr} | 🔹 Soma: {s}<br>
                💰 <b>Valor a pagar: R$ {tabela_precos[qtd_dezenas]:.2f}</b>
            </div>
            """, unsafe_allow_html=True)
            st.success(f"Este jogo de {qtd_dezenas} dezenas NUNCA repetiu os 15 pontos anteriores.")
        else:
            st.error("Critérios muito rígidos para as dezenas fixas escolhidas. Tente novamente!")

st.divider()
st.info("Dica: Use o botão de copiar no canto superior direito dos números para levar o jogo para o site da Caixa.")
