import streamlit as st
import requests, random

# Configurações de Interface
st.set_page_config(page_title="LotoIA Master", page_icon="🔥", layout="centered")

def buscar_dados():
    try:
        # Consulta API de resultados reais
        resp = requests.get("https://lotericas.com.br").json()
        return resp['dezenas'], resp['concurso']
    except:
        # Dados de fallback caso a API falhe
        return ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15"], 0

ultimo_sorteio, concurso = buscar_dados()

# --- LÓGICA DE PADRÕES ---
inicio_alto = False
if ultimo_sorteio and int(ultimo_sorteio[0]) >= 4:
    inicio_alto = True 

st.title("🔥 LotoIA Master: Rastreamento")

# Painel de Monitoramento
col1, col2 = st.columns(2)
with col1:
    st.metric("Último Concurso", concurso)
with col2:
    if inicio_alto:
        st.error("⚠️ PADRÃO: Início Alto (04-06)")
    else:
        st.success("✅ PADRÃO: Início Baixo (01-03)")

modo_ia = st.radio("Configuração da IA:", ["Modo Equilibrado", "Modo Tendência (Início na 06)"])

def gerar_jogo_master(n_dezenas, modo):
    # LISTA CORRIGIDA (O erro estava aqui)
    primos_lista = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    
    for _ in range(10000):
        if modo == "Modo Tendência (Início na 06)":
            universo = list(range(7, 26))
            jogo_base = [6] + random.sample(universo, n_dezenas - 1)
        else:
            universo = list(range(1, 26))
            jogo_base = random.sample(universo, n_dezenas)
        
        jogo = sorted(jogo_base)
        
        pa = len([n for n in jogo if n % 2 == 0])
        pr = len([n for n in jogo if n in primos_lista])
        sm = sum(jogo)
        
        # Filtros Loto Master (Pares 7-10, Primos 4-7, Soma 180-250)
        if (7 <= pa <= 10) and (4 <= pr <= 7) and (180 <= sm <= 250):
            # Garante que não repetiu os 15 pontos do último sorteio
            if len(set(jogo) & set(map(int, ultimo_sorteio))) < 15:
                return jogo, pa, pr, sm
    return None, 0, 0, 0

qtd = st.selectbox("Quantidade de dezenas:", [15, 16, 17])

if st.button("GERAR PALPITE MASTER"):
    res, p, pri, s = gerar_jogo_master(qtd, modo_ia)
    
    if res:
        st.markdown("### 📋 Palpite Gerado:")
        st.code(" - ".join(f"{n:02d}" for n in res), language="text")
        st.info(f"📊 Análise: Pares: {p} | Primos: {pri} | Soma: {s}")
    else:
        st.error("Erro nos filtros. Tente novamente!")
